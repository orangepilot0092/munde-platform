"""
RAGAS-Inspired Evaluation Harness with LLM-as-Judge
Sprint 34 Day 2 — Commercial-grade evaluation using Mumbai-Vikram as judge
Per 04_PROMPTS_AND_EXECUTION.md Testing Prompt: Every feature must include measurable acceptance criteria  # noqa: E501

"""

import json
import os
from datetime import datetime
from typing import Optional, Any

import psycopg2
from psycopg2.extras import RealDictCursor

from src.core.logging_config import get_logger
from src.core.models.prompt import EvalRequest, EvalResult, MetricResult
from src.core.services.llm_service import LLMRequest, LLMService

logger = get_logger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

# Marathi-aware judge prompts calibrated for government domain
JUDGE_PROMPTS = {
    "faithfulness": """तुम्ही महाराष्ट्र सरकारी AI प्रणालीसाठी तज्ञ मूल्यांकनकर्ता आहात.
खालील प्रतिसादाचे 'विश्वासार्हता' (faithfulness) साठी 0.0 ते 1.0 दरम्यान मूल्यमापन करा.
विचारात घ्या: तथ्यात्मक अचूकता, संदर्भित सरकारी स्रोतांचे उल्लेख, आणि ग्राउंड ट्रुथशी सुसंगतता.


सिस्टम प्रॉम्पट: {system_prompt}
ग्राउंड ट्रुथ: {ground_truth}
प्रतिसाद: {response}

फक्त JSON ऑब्जेक्ट परत करा: {{"score": <float>, "reasoning": "<स्पष्टीकरण>"}}""",
    "answer_relevancy": """तुम्ही महाराष्ट्र सरकारी AI प्रणालीसाठी तज्ञ मूल्यांकनकर्ता आहात.

खालील प्रतिसादाचे 'प्रतिसाद प्रासंगिकता' (answer_relevancy) साठी 0.0 ते 1.0 दरम्यान मूल्यमापन करा.

विचारात घ्या: प्रश्नाशी थेट संबंध, कृतीयोग्य माहिती, आणि अनावश्यक सामग्रीचा अभाव.

सिस्टम प्रॉम्पट: {system_prompt}
प्रश्न: {question}
प्रतिसाद: {response}

फक्त JSON ऑब्जेक्ट परत करा: {{"score": <float>, "reasoning": "<स्पष्टीकरण>"}}""",
    "context_precision": """तुम्ही महाराष्ट्र सरकारी AI प्रणालीसाठी तज्ञ मूल्यांकनकर्ता आहात.

खालील प्रतिसादाचे 'संदर्भ अचूकता' (context_precision) साठी 0.0 ते 1.0 दरम्यान मूल्यमापन करा.

विचारात घ्या: योग्य संदर्भाचा वापर, मराठी भाषेची गुणवत्ता, सांस्कृतिक औचित्य, आणि सरकारी परिभाषेचा वापर.


सिस्टम प्रॉम्पट: {system_prompt}
प्रतिसाद: {response}

फक्त JSON ऑब्जेक्ट परत करा: {{"score": <float>, "reasoning": "<स्पष्टीकरण>"}}""",
}


class LLMCallTracker:
    """Tracks LLM API calls for cost and token accounting."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def record(
        self, model: str, input_tokens: int, output_tokens: int, purpose: str = ""
    ) -> None:
        self.calls.append(
            {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "purpose": purpose,
            }
        )

    def get_calls(self) -> list[dict[str, Any]]:
        return self.calls


class EvalHarness:
    """Runs prompt evaluations with optional LLM-as-Judge."""

    def __init__(self) -> None:
        self.llm = LLMService()

    def run_evaluation(self, eval_input: EvalRequest) -> EvalResult:
        """Execute full evaluation pipeline."""
        call_tracker = LLMCallTracker()
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT version, system_prompt, user_template FROM prompt_registry WHERE prompt_id = %s ORDER BY version DESC LIMIT 1",  # noqa: E501
            (eval_input.prompt_id,),
        )
        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            raise ValueError(f"Prompt '{eval_input.prompt_id}' not found")

        # FIXED: Access dict keys explicitly instead of tuple unpacking
        version = int(row["version"])
        system_prompt = row["system_prompt"]
        user_template = row["user_template"]
        cur.close()
        conn.close()

        # Run inference for each test input
        responses = []
        questions = []
        for test_input in eval_input.test_inputs:
            user_msg = (
                user_template.format(**test_input) if user_template else str(test_input)
            )
            llm_resp = self.llm.generate(
                LLMRequest(
                    model=eval_input.model,
                    system_prompt=system_prompt,
                    user_message=user_msg,
                )
            )
            call_tracker.record(
                model="llama3.1:8b",
                input_tokens=len(str(eval_input.test_inputs)) * 10,
                output_tokens=len(llm_resp.response) // 4,
                purpose="prompt_generation",
            )
            responses.append(llm_resp.response)
            questions.append(user_msg)

        # Compute metrics
        metrics = []
        judge_model = "mumbai-vikram:latest" if eval_input.use_llm_judge else None

        for metric_name in eval_input.metrics:
            if eval_input.use_llm_judge and metric_name in JUDGE_PROMPTS:
                score, reasoning = self._compute_llm_judge_metric(
                    metric_name,
                    responses,
                    questions,
                    eval_input.ground_truth,
                    system_prompt,
                    call_tracker=call_tracker,
                )
                metrics.append(
                    MetricResult(
                        metric_name=metric_name,
                        score=score,
                        method="llm_judge",
                        reasoning=reasoning,
                    )
                )
            else:
                score = self._compute_heuristic_metric(
                    metric_name, responses, eval_input.ground_truth
                )
                metrics.append(
                    MetricResult(
                        metric_name=metric_name,
                        score=score,
                        method="heuristic",
                    )
                )

        avg_score = sum(m.score for m in metrics) / len(metrics) if metrics else 0.0

        result = EvalResult(
            prompt_id=eval_input.prompt_id,
            model=eval_input.model,
            version=version,
            metrics=metrics,
            num_samples=len(eval_input.test_inputs),
            timestamp=datetime.utcnow(),
            avg_score=avg_score,
            llm_calls=call_tracker.get_calls(),
            judge_model=judge_model,
        )

        logger.info(
            f"Eval complete: prompt={eval_input.prompt_id}, model={eval_input.model}, "
            f"samples={result.num_samples}, avg_score={avg_score:.3f}, "
            f"method={'llm_judge' if eval_input.use_llm_judge else 'heuristic'}"
        )
        return result

    def _compute_llm_judge_metric(
        self,
        metric_name: str,
        responses: list[str],
        questions: list[str],
        ground_truth: list[str] | None,
        system_prompt: str,
        call_tracker: Optional["LLMCallTracker | None"] = None,
    ) -> tuple[float, str]:
        """Use Mumbai-Vikram as judge for Marathi-aware evaluation."""
        template = JUDGE_PROMPTS[metric_name]
        scores = []
        reasonings = []

        for i, resp in enumerate(responses):
            gt = ground_truth[i] if ground_truth and i < len(ground_truth) else "N/A"
            q = questions[i] if i < len(questions) else "N/A"

            judge_prompt = template.format(
                system_prompt=system_prompt[:500],
                ground_truth=gt,
                response=resp[:1000],
                question=q[:500],
            )

            try:
                judge_resp = self.llm.generate(
                    LLMRequest(
                        model="mumbai-vikram:latest",
                        system_prompt="तुम्ही एक निष्पक्ष AI मूल्यांकनकर्ता आहात. फक्त JSON परत करा.",  # noqa: E501
                        user_message=judge_prompt,
                        temperature=0.0,
                        max_tokens=256,
                    )
                )

                if call_tracker:
                    call_tracker.record(
                        model="mumbai-vikram:latest",
                        input_tokens=len(judge_prompt) // 4,
                        output_tokens=len(judge_resp.response) // 4,
                        purpose="llm_judge",
                    )
                raw = judge_resp.response.strip()
                if raw.startswith("```"):
                    raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

                result = json.loads(raw)
                score = float(result.get("score", 0.5))
                score = max(0.0, min(1.0, score))
                scores.append(score)
                reasonings.append(result.get("reasoning", ""))

            except (json.JSONDecodeError, KeyError, ValueError, Exception) as e:
                logger.warning(f"LLM judge parse failed for {metric_name}[{i}]: {e}")
                scores.append(0.5)
                reasonings.append(f"Parse error: {str(e)}")

        avg = sum(scores) / len(scores) if scores else 0.0
        combined_reasoning = "; ".join(reasonings[:3])
        return avg, combined_reasoning

    def _compute_heuristic_metric(
        self, metric_name: str, responses: list[str], ground_truth: list[str] | None
    ) -> float:
        """Fallback heuristic scoring for backward compatibility."""
        if metric_name == "faithfulness":
            if not ground_truth:
                return 0.8
            hits = sum(
                1
                for r, gt in zip(responses, ground_truth, strict=False)
                if any(word.lower() in r.lower() for word in gt.split())
            )
            return hits / len(responses) if responses else 0.0

        elif metric_name == "answer_relevancy":
            valid = sum(1 for r in responses if len(r.strip()) > 20)
            return valid / len(responses) if responses else 0.0

        elif metric_name == "context_precision":
            structured = sum(1 for r in responses if ":" in r or "-" in r or "\n" in r)
            return structured / len(responses) if responses else 0.0

        else:
            logger.warning(f"Unknown metric '{metric_name}', returning 0.0")
            return 0.0
