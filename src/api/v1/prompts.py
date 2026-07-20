"""
Prompt Registry & Evaluation API Endpoints
Sprint 34 — Prompt Management & Evaluation Framework
ROUTE ORDER MATTERS: Literal routes MUST precede parameterized routes in FastAPI.
"""

import json
from typing import Any
import os

import psycopg2
from fastapi import APIRouter, HTTPException, Request
from psycopg2.extras import RealDictCursor

from src.core.limiter import limiter
from src.core.logging_config import get_logger
from src.core.models.prompt import (
    EvalRequest,
    EvalResult,
    PromptResponse,
)
from src.core.services.eval_harness import EvalHarness
from src.core.services.llm_service import LLMService

logger = get_logger(__name__)

router = APIRouter(prefix="/prompts", tags=["Prompt Management"])

DATABASE_URL = os.environ.get("DATABASE_URL")
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")


def _get_redis_settings() -> Any:
    """Parse REDIS_URL into arq.RedisSettings."""
    from arq.connections import RedisSettings

    # Parse redis://host:port/db format
    url = REDIS_URL.replace("redis://", "")
    parts = url.split("/")
    host_port = parts[0]
    db = int(parts[1]) if len(parts) > 1 else 0
    if ":" in host_port:
        host, port_str = host_port.split(":")
        port: int = int(port_str)
    else:
        host = host_port
        port = 6379
    return RedisSettings(host=host, port=port, database=db)


# ─── LITERAL ROUTES FIRST ────────────────────────────────────────────────────


@router.get("/models")
def list_models() -> dict[str, Any]:
    """List available AI Node models and registry status."""
    try:
        return LLMService.health_check()
    except Exception as e:
        logger.error(f"list_models failed: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/eval/run")
@limiter.limit("5/minute")  # type: ignore[misc]
async def run_evaluation(
    request: Request, eval_request: EvalRequest
) -> EvalResult | dict[str, Any]:
    """Execute prompt evaluation. Returns job_id for async, or result for sync."""
    eval_input = EvalRequest(
        prompt_id=eval_request.prompt_id,
        model=eval_request.model,
        test_inputs=eval_request.test_inputs,
        ground_truth=eval_request.ground_truth,
        metrics=eval_request.metrics,
        use_llm_judge=getattr(eval_request, "use_llm_judge", True),
    )

    if getattr(eval_request, "async_mode", False):
        try:
            from arq import create_pool

            redis_settings = _get_redis_settings()
            pool = await create_pool(redis_settings)
            job = await pool.enqueue_job("run_eval_job", eval_input.model_dump())
            return {
                "status": "queued",
                "job_id": job.job_id,
                "poll_url": f"/api/v1/prompts/eval/status/{job.job_id}",
            }
        except Exception as e:
            logger.error(f"Failed to enqueue eval job: {e}")
            raise HTTPException(status_code=503, detail=f"Queue unavailable: {str(e)}")
    else:
        try:
            harness = EvalHarness()
            result = harness.run_evaluation(eval_input)
            return result
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except Exception as e:
            logger.error(f"run_evaluation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


@router.get("/eval/status/{job_id}")
async def get_eval_status(job_id: str) -> dict[str, Any]:
    """Poll async evaluation result."""
    try:
        from arq import create_pool

        redis_settings = _get_redis_settings()
        pool = await create_pool(redis_settings)

        result_key = f"eval_result:{job_id}"
        result_data = await pool.get(result_key)
        if result_data:
            return json.loads(result_data)  # type: ignore[no-any-return]

        queued = await pool.queued_jobs()
        if any(j.job_id == job_id for j in queued):
            return {"status": "queued", "job_id": job_id}

        return {"status": "not_found", "job_id": job_id}
    except Exception as e:
        logger.error(f"get_eval_status failed: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/", response_model=list[PromptResponse])
def list_prompts(
    domain: str | None = None, category: str | None = None
) -> list[PromptResponse]:
    """List all prompts with optional domain/category filter."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = "SELECT * FROM prompt_registry WHERE version = (SELECT MAX(version) FROM prompt_registry pr2 WHERE pr2.prompt_id = prompt_registry.prompt_id)"  # noqa: E501
    params = []
    conditions = []

    if domain:
        conditions.append("domain = %s")
        params.append(domain)
    if category:
        conditions.append("category = %s")
        params.append(category)

    if conditions:
        query += " AND " + " AND ".join(conditions)

    query += " ORDER BY domain, prompt_id"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows  # type: ignore[no-any-return]


# ─── PARAMETERIZED ROUTES LAST ───────────────────────────────────────────────


@router.get("/{prompt_id}", response_model=PromptResponse)
def get_prompt(prompt_id: str, version: int | None = None) -> PromptResponse:
    """Get a specific prompt by ID and optional version."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if version:
        cur.execute(
            "SELECT * FROM prompt_registry WHERE prompt_id = %s AND version = %s",
            (prompt_id, version),
        )
    else:
        cur.execute(
            "SELECT * FROM prompt_registry WHERE prompt_id = %s ORDER BY version DESC LIMIT 1",  # noqa: E501
            (prompt_id,),
        )

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Prompt '{prompt_id}' not found")
    return row  # type: ignore[no-any-return]
