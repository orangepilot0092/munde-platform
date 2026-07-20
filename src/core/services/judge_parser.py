"""
Robust Judge Output Parser
Sprint 35 Day 2 — Regex fallback + structured validation for LLM judge outputs
Target: >95% parse success rate
"""

import json
import re

from pydantic import BaseModel, Field, ValidationError

from src.core.logging_config import get_logger

logger = get_logger(__name__)


class JudgeOutput(BaseModel):
    """Validated judge response schema."""

    score: float = Field(..., ge=0.0, le=1.0)
    reasoning: str = Field(..., min_length=1)


# Regex patterns ordered by specificity (most specific first)
_JUDGE_PATTERNS = [
    # Pattern 1: Clean JSON object
    re.compile(
        r'\{[^{}]*"score"\s*:\s*[\d.]+[^{}]*"reasoning"\s*:\s*"[^"]*"[^{}]*\}',
        re.DOTALL,
    ),
    # Pattern 2: JSON with markdown code fences
    re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL),
    # Pattern 3: Score as number followed by reasoning text
    re.compile(
        r"(?:score|विश्वासार्हता|faithfulness)\s*[:=]?\s*([\d.]+)\s*[,;\n]\s*"
        r"(?:reasoning|स्पष्टीकरण|कारण)\s*[:=]?\s*(.+)",
        re.IGNORECASE | re.DOTALL,
    ),
    # Pattern 4: Standalone float at start of response
    re.compile(r"^\s*([\d.]+)\s*[-–:]\s*(.+)", re.MULTILINE),
]


def parse_judge_output(
    raw: str, metric_name: str = "faithfulness"
) -> JudgeOutput | None:
    """
    Parse LLM judge output with cascading fallback strategies.

    Returns validated JudgeOutput or None if all strategies fail.
    """
    if not raw or not raw.strip():
        logger.warning(f"[JudgeParser] Empty response for {metric_name}")
        return None

    # Strategy 1: Direct JSON parse
    try:
        data = json.loads(raw)
        result = JudgeOutput(**data)
        logger.debug(f"[JudgeParser] Direct JSON parse succeeded for {metric_name}")
        return result
    except (json.JSONDecodeError, ValidationError) as e:
        logger.debug(f"[JudgeParser] Direct JSON failed: {e}")

    # Strategy 2: Regex extraction cascade
    for i, pattern in enumerate(_JUDGE_PATTERNS):
        match = pattern.search(raw)
        if match:
            try:
                groups = match.groups()
                if len(groups) == 1:
                    # Single group = wrapped JSON, try parsing inner content
                    inner = json.loads(groups[0])
                    result = JudgeOutput(**inner)
                elif len(groups) == 2:
                    # Two groups = score + reasoning extracted separately
                    score_val = float(groups[0])
                    reasoning_val = groups[1].strip().rstrip('"').rstrip("'")
                    result = JudgeOutput(score=score_val, reasoning=reasoning_val)
                else:
                    continue

                logger.info(
                    f"[JudgeParser] Regex pattern {i + 1} succeeded for "
                    f"{metric_name}: score={result.score}"
                )
                return result
            except (ValueError, ValidationError, json.JSONDecodeError) as e:
                logger.debug(f"[JudgeParser] Regex pattern {i + 1} failed: {e}")
                continue

    # Strategy 3: Last resort — extract any float as score, rest as reasoning
    float_match = re.search(r"([\d.]+)", raw)
    if float_match:
        try:
            score_val = float(float_match.group(1))
            if 0.0 <= score_val <= 1.0:
                reasoning_val = raw.replace(float_match.group(1), "").strip()[:500]
                if not reasoning_val:
                    reasoning_val = (
                        "Score extracted via fallback; reasoning unavailable"
                    )
                result = JudgeOutput(score=score_val, reasoning=reasoning_val)
                logger.warning(
                    f"[JudgeParser] Last-resort float extraction for "
                    f"{metric_name}: score={score_val}"
                )
                return result
        except ValueError:
            pass

    logger.error(
        f"[JudgeParser] ALL PARSE STRATEGIES FAILED for {metric_name}. "
        f"Raw: {raw[:200]}..."
    )
    return None
