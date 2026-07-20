"""
Async Evaluation Worker
Sprint 35 Day 2 — Non-blocking LLM-as-Judge evaluation via ARQ + Redis
Per 02_ARCHITECTURE_AND_INFRA.md Layer 9: Background jobs for long-running tasks
"""

import json
from src.core.models.prompt import EvalRequest
from typing import Any
import os
import time
from datetime import UTC, datetime

from arq.connections import RedisSettings

from src.core.logging_config import get_logger
from src.core.observability import EvalCostTracker, request_id_var
from src.core.services.eval_harness import EvalHarness

logger = get_logger(__name__)

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")


def _parse_redis_url(url: str) -> RedisSettings:
    """Parse REDIS_URL into arq.RedisSettings."""
    cleaned = url.replace("redis://", "")
    parts = cleaned.split("/")
    host_port = parts[0]
    db = int(parts[1]) if len(parts) > 1 else 0
    if ":" in host_port:
        host, port_str = host_port.split(":")
        port: int = int(port_str)
    else:
        host = host_port
        port = 6379
    return RedisSettings(host=host, port=port, database=db)


async def run_eval_job(
    ctx: dict[str, Any], eval_input_dict: dict[str, Any]
) -> dict[str, object]:
    """Background task for prompt evaluation with retry, DLQ, and cost tracking."""
    job_id = ctx.get("job_id", "unknown")
    req_token = request_id_var.set(f"worker-{job_id}")
    start_time = time.perf_counter()

    try:
        eval_input = EvalRequest(**eval_input_dict)
        harness: EvalHarness = EvalHarness()

        logger.info(
            f"[Worker:{job_id}] Starting eval: prompt={eval_input.prompt_id}, "
            f"model={eval_input.model}, samples={len(eval_input.test_inputs)}"
        )
        result = harness.run_evaluation(eval_input)

        # Calculate cost metrics
        duration_ms = (time.perf_counter() - start_time) * 1000
        cost_data = EvalCostTracker.aggregate_eval_cost(
            getattr(result, "llm_calls", [])
        )

        # Store result in Redis for polling (TTL 1 hour)
        from arq import create_pool

        redis_settings = _parse_redis_url(REDIS_URL)
        pool = await create_pool(redis_settings)
        result_key = f"eval_result:{job_id}"
        await pool.set(result_key, result.model_dump_json(), ex=3600)

        logger.info(
            f"[Worker:{job_id}] Eval complete: avg_score={result.avg_score:.3f}, "
            f"tokens={cost_data['total_tokens']}, cost=${cost_data['total_cost_usd']:.4f}, "  # noqa: E501
            f"duration={duration_ms:.0f}ms"
        )

        # Store enriched result with cost metrics
        from arq import create_pool

        redis_settings = _parse_redis_url(REDIS_URL)
        pool = await create_pool(redis_settings)
        result_key = f"eval_result:{job_id}"
        # Use Pydantic serialization to handle datetime objects
        result_json = result.model_dump(mode="json")
        result_json["cost"] = cost_data
        result_json["duration_ms"] = round(duration_ms, 1)
        await pool.set(result_key, json.dumps(result_json), ex=3600)

        return {
            "job_id": job_id,
            "status": "completed",
            "avg_score": result.avg_score,
            "cost_usd": cost_data["total_cost_usd"],
            "total_tokens": cost_data["total_tokens"],
            "duration_ms": round(duration_ms, 1),
        }

    except Exception as e:
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.error(
            f"[Worker:{job_id}] Eval failed after {duration_ms:.0f}ms: {e}",
            exc_info=True,
        )
        # Store failure in DLQ key for inspection
        from arq import create_pool

        redis_settings = _parse_redis_url(REDIS_URL)
        pool = await create_pool(redis_settings)
        dlq_key = f"eval_dlq:{job_id}"
        await pool.set(
            dlq_key,
            json.dumps(
                {
                    "error": str(e),
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            ),
            ex=86400,  # 24h TTL
        )
        raise  # Re-raise so ARQ retry logic engages
    finally:
        request_id_var.reset(req_token)


class WorkerSettings:
    """ARQ worker configuration with retry and monitoring."""

    functions = [run_eval_job]
    redis_settings = _parse_redis_url(REDIS_URL)
    max_jobs = 4
    job_timeout = 300  # 5 min max per eval
    retry_jobs = True
    max_tries = 3
    expires_extra_ms = 60000  # 1 min grace period
