"""
Prometheus Metrics for Project Sahyadri
Sprint 35 Day 3 — Queue depth, processing latency, failure rates
Per 02_ARCHITECTURE_AND_INFRA.md Layer 4: Monitoring strategy
"""

from fastapi import Response
from fastapi.routing import APIRouter
from prometheus_client import Counter, Gauge, Histogram, generate_latest

router = APIRouter(tags=["metrics"])

# Evaluation metrics
eval_jobs_total = Counter(
    "sahyadri_eval_jobs_total",
    "Total evaluation jobs processed",
    ["status", "model"],
)

eval_duration_seconds = Histogram(
    "sahyadri_eval_duration_seconds",
    "Evaluation job processing duration",
    ["model"],
    buckets=[1, 5, 10, 30, 60, 120, 300],
)

eval_cost_usd = Counter(
    "sahyadri_eval_cost_usd_total",
    "Total evaluation cost in USD",
    ["model"],
)

eval_tokens_total = Counter(
    "sahyadri_eval_tokens_total",
    "Total tokens consumed by evaluations",
    ["model", "direction"],  # direction: input/output
)

eval_parse_failures = Counter(
    "sahyadri_eval_parse_failures_total",
    "Judge output parse failures",
    ["metric_name"],
)

# Worker health metrics
worker_queue_depth = Gauge(
    "sahyadri_worker_queue_depth",
    "Current number of pending evaluation jobs",
)

worker_active_jobs = Gauge(
    "sahyadri_worker_active_jobs",
    "Currently processing evaluation jobs",
)


@router.get("/metrics")
async def prometheus_metrics() -> Response:
    """Expose Prometheus-compatible metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
