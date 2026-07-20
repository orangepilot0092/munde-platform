"""
Production FastAPI router for RAG Queries.
Includes RBAC middleware, structured logging, PII guardrails, and evaluation hooks.
Aligned with Engineering Constitution: API-first, Security by Design, Explainability.
"""

import logging
import re
import time
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.search import SearchService
from src.core.services.llm_service import LLMRequest, LLMService
from src.schemas.rag_query import (
    Citation,
    RAGQueryRequest,
    RAGQueryResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/intelligence", tags=["RAG Intelligence"])


# --- RBAC Dependency ---
class UserContext:
    def __init__(self, user_id: str, role: str, department: Optional[str] = None):
        self.user_id = user_id
        self.role = role
        self.department = department


async def get_current_user(request: Request) -> UserContext:
    """Dependency to extract and validate user context from request headers."""
    auth_header = request.headers.get("X-User-Role")
    user_id = request.headers.get("X-User-ID", "anonymous")
    department = request.headers.get("X-User-Department")

    if not auth_header or auth_header not in ["officer", "admin", "citizen"]:
        logger.warning("Unauthorized access attempt", extra={"user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication credentials",
        )

    return UserContext(user_id=user_id, role=auth_header, department=department)


def _redact_pii(text: str) -> str:
    """
    Basic PII redaction guardrail for logging.
    In production, this would use Microsoft Presidio for robust NER-based redaction.
    """
    # Simple regex patterns for demonstration (e.g., phone numbers, emails)
    text = re.sub(r"\b\d{10}\b", "[REDACTED_PHONE]", text)
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]", text
    )
    return text


def _evaluate_faithfulness(query: str, context: str, answer: str) -> float:
    """
    Evaluates if the answer is faithful to the provided context.
    In production, this calls src.core.services.eval_harness.evaluate_faithfulness.
    For now, we use a heuristic baseline to ensure the pipeline is wired.
    """
    # Heuristic: Check if key terms from the answer exist in the context
    # Production: Replace with LLM-as-a-Judge or NLI model via eval_harness
    answer_words = set(re.findall(r"\w+", answer.lower()))
    context_words = set(re.findall(r"\w+", context.lower()))

    if not answer_words:
        return 0.0

    overlap = len(answer_words.intersection(context_words))
    faithfulness_score = min(overlap / len(answer_words), 1.0)

    # Boost score if it's a known fallback response
    if "context does not contain the answer" in answer.lower():
        return 0.95

    return round(faithfulness_score, 2)


@router.post(
    "/query",
    response_model=RAGQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute a RAG Query",
    description="Answers a natural language query using trusted Intelligence Assets, with mandatory citations and confidence scores.",
)
async def execute_rag_query(
    request: RAGQueryRequest,
    http_request: Request,
    current_user: UserContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RAGQueryResponse:
    """
    Production RAG endpoint with guardrails and evaluation.
    """
    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Guardrail: Redact PII from logs
    safe_query = _redact_pii(request.query)

    logger.info(
        "rag_query_started",
        extra={
            "request_id": request_id,
            "user_id": current_user.user_id,
            "role": current_user.role,
            "query_length": len(safe_query),
            "domain": request.domain,
        },
    )

    try:
        # 1. Initialize Services
        search_service = SearchService(db=db)

        # 2. Fetch Context (Vector/Hybrid Search)
        vector_results = search_service.search_datasets(
            query=request.query,
            domain=request.domain or "",
            limit=request.max_results,
        )

        if not vector_results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No relevant intelligence assets found for this query.",
            )

        # 3. Build Context String for LLM
        context_chunks = []
        citations = []
        for idx, item in enumerate(vector_results):
            context_chunks.append(
                f"[{idx + 1}] Source: {item.get('name', 'Unknown')}\nContent: {item.get('description', '')}"
            )
            citations.append(
                Citation(
                    source_id=str(item.get("id", f"unknown_{idx}")),
                    source_name=item.get("name", "Unknown Source"),
                    source_type=item.get("type", "dataset"),
                    relevance_score=float(
                        item.get("vec_score", item.get("kw_score", 0.5))
                    ),
                )
            )

        context_text = "\n\n".join(context_chunks)

        # 4. Generate Response via LLM Service
        system_prompt = (
            "You are an AI assistant for Project Sahyadri, a sovereign intelligence platform for Maharashtra. "
            "Answer the user's query accurately using ONLY the provided context. "
            "If the context does not contain the answer, state clearly: 'The provided context does not contain sufficient information to answer this query.' "
            "Always cite the specific source name when mentioning facts."
        )

        llm_request = LLMRequest(
            model="sovereign-llm-v1",
            system_prompt=system_prompt,
            user_message=f"Query: {safe_query}\n\nContext:\n{context_text}",
            temperature=0.1,  # Low temperature for factual accuracy
            max_tokens=1024,
        )

        llm_response = LLMService.generate(llm_request)
        answer_text = getattr(llm_response, "response", str(llm_response))

        # 5. Evaluate Faithfulness (Guardrail against hallucination)
        faithfulness_score = _evaluate_faithfulness(
            safe_query, context_text, answer_text
        )

        # 6. Calculate Final Confidence Score
        max_relevance = max((c.relevance_score for c in citations), default=0.5)
        # Confidence is a blend of retrieval relevance and generation faithfulness
        confidence_score = round((max_relevance * 0.6) + (faithfulness_score * 0.4), 2)

        # 7. Calculate Latency
        latency_ms = round((time.time() - start_time) * 1000, 2)

        response = RAGQueryResponse(
            answer=answer_text,
            confidence_score=confidence_score,
            citations=citations,
            reasoning_steps=[
                "Parsed and sanitized natural language query",
                "Executed hybrid semantic/keyword search",
                "Retrieved top relevant Intelligence Assets",
                "Synthesized response via sovereign LLM",
                "Validated faithfulness against retrieved context",
            ],
            metadata={
                "request_id": request_id,
                "latency_ms": latency_ms,
                "context_sources_count": len(citations),
                "model_used": llm_request.model,
                "faithfulness_score": faithfulness_score,
            },
        )

        logger.info(
            "rag_query_completed",
            extra={
                "request_id": request_id,
                "latency_ms": latency_ms,
                "confidence_score": confidence_score,
                "faithfulness_score": faithfulness_score,
                "citations_count": len(citations),
            },
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "rag_query_failed",
            extra={
                "request_id": request_id,
                "error": _redact_pii(str(e)),
            },
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while processing the intelligence query.",
        )
