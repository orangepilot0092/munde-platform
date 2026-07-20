# System Architecture Overview

Project Sahyadri is built on a modular, microservices-ready architecture designed for scalability and resilience.

```mermaid
graph TD
    A[Client Apps / Citizens] -->|HTTPS| B(FastAPI Gateway)
    B --> C{Auth & RBAC}
    C -->|Valid Token| D[Domain Services]
    C -->|Invalid| E[401/403 Response]
    D --> F[(PostgreSQL + PostGIS)]
    D --> G[(Redis Cache)]
    D --> H[(MinIO Object Store)]
    I[Prometheus] -->|Scrape Metrics| B
    J[Grafana] -->|Visualize| I
    K[Audit Logger] -->|Write Logs| F

### Step 3: Create API Reference Entry Point (`docs/api/core.md`)

This file will auto-generate documentation from your Python source code.

```bash
mkdir -p docs/api
cat > docs/api/core.md << 'EOF'
# Core API Services

The core services provide the foundational building blocks for the Sahyadri platform, including health checks, authentication, and data ingestion utilities.

::: src.core.main
    options:
      show_root_heading: false
      show_source: false

::: src.core.auth
    options:
      show_root_heading: true
      show_source: true

::: src.core.health
    options:
      show_root_heading: true
      show_source: true
