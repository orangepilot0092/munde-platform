# ADR-0005: Structured JSON Logging and Prometheus Metrics for Observability

## Status
Accepted

## Context
The Sahyadri Engineering Constitution states: *"Everything observable: If it’s not monitored, it doesn’t exist."* Standard print statements or unstructured logs are insufficient for production debugging and SLO tracking.

## Decision
1. Integrate **`structlog`** to output machine-readable, structured JSON logs containing `method`, `path`, `status_code`, `duration_ms`, and `client_ip`.
2. Integrate **`prometheus-fastapi-instrumentator`** to automatically expose a `/metrics` endpoint tracking HTTP request counts, latencies, and Python GC stats.

## Consequences
- **Pros:** Ready for immediate ingestion by Grafana Loki/Prometheus. Enables precise SLO tracking and rapid incident debugging.
- **Cons:** Slight overhead in log serialization, which is negligible compared to the operational benefits.
