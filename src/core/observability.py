"""
Observability Foundation
Sprint 35 Day 3 — Structured logging, request ID propagation, cost tracking
Per 02_ARCHITECTURE_AND_INFRA.md Layer 4: Observability by default
"""

import time
import uuid
from contextvars import ContextVar
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.core.logging_config import get_logger

logger = get_logger(__name__)

# Context variables for request-scoped observability
request_id_var: ContextVar[str] = ContextVar("request_id", default="")
actor_var: ContextVar[str] = ContextVar("actor", default="SYSTEM")


def generate_request_id() -> str:
    """Generate a unique request ID for tracing."""
    return str(uuid.uuid4())[:12]


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Injects request_id into all logs and response headers."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        req_id = request.headers.get("X-Request-ID", generate_request_id())
        token = request_id_var.set(req_id)

        start_time = time.perf_counter()
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={"request_id": req_id},
        )

        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"status={response.status_code} duration={duration_ms:.1f}ms",
                extra={"request_id": req_id},
            )

            response.headers["X-Request-ID"] = req_id
            response.headers["X-Response-Time-Ms"] = f"{duration_ms:.1f}"
            return response

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"error={e} duration={duration_ms:.1f}ms",
                exc_info=True,
                extra={"request_id": req_id},
            )
            raise
        finally:
            request_id_var.reset(token)


class EvalCostTracker:
    """Tracks token usage and cost per evaluation job."""

    # Pricing per 1M tokens (USD) — update when models change
    MODEL_PRICING: dict[str, dict[str, float]] = {
        "llama3.1:8b": {"input": 0.0, "output": 0.0},  # Self-hosted = $0
        "mumbai-vikram:latest": {"input": 0.0, "output": 0.0},  # Self-hosted
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
    }

    @classmethod
    def calculate_cost(
        cls,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> dict[str, Any]:
        """Calculate cost for a single LLM call."""
        pricing = cls.MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost

        return {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
        }

    @classmethod
    def aggregate_eval_cost(cls, calls: list[dict[str, Any]]) -> dict[str, Any]:
        """Aggregate costs across multiple LLM calls in one evaluation."""
        total_input = sum(c.get("input_tokens", 0) for c in calls)
        total_output = sum(c.get("output_tokens", 0) for c in calls)
        total_cost = sum(c.get("total_cost_usd", 0.0) for c in calls)

        models_used = list({c.get("model", "unknown") for c in calls})

        return {
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_input + total_output,
            "total_cost_usd": round(total_cost, 6),
            "num_llm_calls": len(calls),
            "models_used": models_used,
        }
