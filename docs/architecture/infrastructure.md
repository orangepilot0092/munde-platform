# Infrastructure Architecture

## Node Roles

### PC Node (Workstation)
- **Role:** Operational Backbone
- **Components:** PostgreSQL, PostGIS, MinIO, Redis, ETL Engines, API Services.
- **Hardware:** Ryzen 9, 64GB RAM, RTX 5060 Ti.

### AI Node (DGX Spark)
- **Role:** Intelligence Engine
- **Components:** LLM Inference, Embedding Generation, OCR, Vision Models.
- **Hardware:** NVIDIA GB10 Grace Blackwell, 128GB Unified Memory.

## Networking
- Internal communication via Docker networks.
- External access via Reverse Proxy (Caddy/Traefik).

## Storage Strategy
- **Structured:** PostgreSQL + PostGIS.
- **Unstructured:** MinIO (S3-compatible).
- **Vector:** pgvector extension in PostgreSQL.

## Secrets Management
- Environment variables for local development.
- HashiCorp Vault or Docker Secrets for production.
