# Observability & Monitoring

Project Sahyadri implements structured observability across all services per [02_ARCHITECTURE_AND_INFRA.md](../review/architecture-validation.md) Layer 4.

## Request Tracing

All API requests are assigned a unique `X-Request-ID` header via `ObservabilityMiddleware`. This ID propagates through:

- HTTP response headers (`X-Request-ID`, `X-Response-Time-Ms`)
- Structured log entries (`request_id` field)
- Async worker jobs (`worker-{job_id}` format)

## Prometheus Metrics

The `/metrics` endpoint exposes Prometheus-compatible metrics:

| Metric | Type | Description |
|--------|------|-------------|
| `sahyadri_eval_jobs_total` | Counter | Total evaluation jobs processed by status/model |
| `sahyadri_eval_duration_seconds` | Histogram | Evaluation job processing duration |
| `sahyadri_eval_cost_usd_total` | Counter | Total evaluation cost in USD |
| `sahyadri_eval_tokens_total` | Counter | Total tokens consumed by evaluations |
| `sahyadri_eval_parse_failures_total` | Counter | Judge output parse failures by metric |
| `sahyadri_worker_queue_depth` | Gauge | Pending evaluation jobs in queue |
| `sahyadri_worker_active_jobs` | Gauge | Currently processing evaluation jobs |

### Scraping Configuration

```yaml
scrape_configs:
  - job_name: sahyadri-platform
    scrape_interval: 15s
    static_configs:
      - targets: [localhost:8001]
    metrics_path: /metrics
```

## Cost Tracking

Every evaluation job tracks LLM call metadata via `LLMCallTracker`:

- **Model**: Which model was called (e.g., `llama3.1:8b`, `mumbai-vikram:latest`)
- **Tokens**: Estimated input/output tokens (character-based for self-hosted models)
- **Cost**: USD cost based on `EvalCostTracker.MODEL_PRICING`
- **Duration**: Wall-clock time in milliseconds

Self-hosted models (`llama3.1:8b`, `mumbai-vikram`) are priced at $0.00. Update `MODEL_PRICING` in `src/core/observability.py` when cloud models are added.

## Structured Logging

All services use JSON-structured logging via `src.core.logging`:

```json
{
  "asctime": "2026-07-10T14:57:24,606",
  "levelname": "INFO",
  "name": "src.core.services.eval_worker",
  "message": "[Worker:abc123] Eval complete: avg_score=0.900, tokens=1200, cost=\$0.0000, duration=10328ms",
  "request_id": "worker-abc123"
}
```

## Async Worker Monitoring

The ARQ eval worker (`docker-eval-worker-1`) provides:

- **Health checks**: Redis connectivity via `redis.ping()`
- **Job tracking**: Results stored in Redis with 1-hour TTL (`eval_result:{job_id}`)
- **Dead Letter Queue**: Failed jobs stored in `eval_dlq:{job_id}` for debugging
- **Cost enrichment**: Worker adds `cost`, `duration_ms`, `llm_calls` to results before storage
