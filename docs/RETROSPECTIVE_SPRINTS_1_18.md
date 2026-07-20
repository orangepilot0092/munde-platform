# Project Sahyadri: Engineering Journey & Retrospective (Sprints 1–18)

## Executive Summary
This document captures the engineering journey, architectural decisions, and technical challenges resolved during **Phase 1 (Engineering Foundation)**, **Phase 2 (Maharashtra Data Atlas)**, and the initial stages of **Phase 3 (Core Data Platform)**. 

By Sprint 18, Project Sahyadri successfully established a unified, production-ready data platform capable of handling relational data, geospatial boundaries, object storage, vector embeddings, and OCR-driven document processing.

---

## Key Engineering Challenges & Resolutions

### 1. Unifying Orchestration Storage (Dagster & PostgreSQL)
* **The Problem:** Dagster’s default local storage relies on SQLite. Inside Docker containers, this caused `sqlite3.OperationalError: unable to open database file` due to strict filesystem permissions. Furthermore, when we attempted to point Dagster to our main PostgreSQL database, its internal Alembic migrations collided with our application's migrations, resulting in `Can't locate revision identified by...` errors.
* **The Resolution:** We abandoned SQLite entirely to adhere to the platform's "Unified Storage" principle. We created a `dagster.yaml` configuration file to route `run_storage`, `event_log_storage`, and `schedule_storage` to PostgreSQL. To resolve the Alembic collision, we isolated Dagster's migration state, ensuring the orchestration engine and the application schema could coexist in the same database instance without interfering with each other's version history.

### 2. Python 3.14 Typing Evaluation vs. Pydantic v2
* **The Problem:** The host machine (PC Node) was running Python 3.14. When attempting to run Dagster CLI commands locally, we encountered a `PydanticUserError: Field 'base_dir' requires a type annotation`. This was caused by PEP 749 (changes to lazy type evaluation in Python 3.14) breaking the internal Pydantic v2 models that Dagster relies upon.
* **The Resolution:** We enforced strict environment isolation. The Docker containers were locked to `python:3.11-slim` to guarantee stability. For local host testing and rapid iteration, we bypassed the Dagster CLI wrapper and authored a standalone execution script (`scripts/test_ocr_pipeline.py`). This allowed us to validate the core ETL logic natively on the host machine without triggering the incompatible Pydantic/Dagster import chain.

### 3. System-Level Dependencies for OCR (Tesseract & Poppler)
* **The Problem:** The OCR pipeline (`pytesseract` and `pdf2image`) requires underlying C-libraries and OS-level binaries that are not present in lightweight Python Docker images. This resulted in silent failures and `PDFInfoNotInstalledError` during asset materialization.
* **The Resolution:** We updated the application `Dockerfile` and Dagster container startup scripts to include `apt-get install -y tesseract-ocr poppler-utils gcc`. Additionally, we established a **"Host-Machine Fallback"** pattern—installing these tools natively on the Ubuntu PC Node via `sudo apt install`. This drastically reduced the feedback loop for developers testing OCR logic without waiting for Docker image rebuilds.

### 4. Volatile External Test Data
* **The Problem:** The initial sample PDF URLs sourced from standard W3C and educational test servers began returning `404 Not Found` or `403 Forbidden` errors, breaking the automated validation steps for Sprint 18.
* **The Resolution:** We switched the test artifact to the **Mozilla `pdf.js-sample-files`** repository on GitHub. This ensured a permanent, version-controlled, and highly available test document (`helloworld.pdf`) to guarantee pipeline stability during CI/CD runs and local testing.

### 5. Integrating PostGIS and pgvector in a Single Instance
* **The Problem:** The platform required both Geospatial capabilities (PostGIS) and Semantic Search capabilities (`pgvector`). Standard PostgreSQL Docker images include neither, and official extension images rarely include both out-of-the-box.
* **The Resolution:** We engineered a custom database Dockerfile (`infra/db/Dockerfile`) extending the official `postgis/postgis:15-3.3` image. By adding a build step to compile and install `postgresql-15-pgvector`, we successfully unified Relational, Geospatial, and Vector search capabilities into a single PostgreSQL instance. This significantly reduced operational complexity and infrastructure costs.

---

## Architectural Milestones Achieved

| Layer | Milestone | Status |
| :--- | :--- | :---: |
| **Storage** | PostgreSQL, PostGIS, MinIO, Redis fully orchestrated via Docker Compose. | ✅ |
| **Orchestration** | Dagster ETL engine running with PostgreSQL-backed persistent storage. | ✅ |
| **Knowledge Graph** | Relational graph schema populated with Maharashtra administrative hierarchy. | ✅ |
| **Geospatial** | PostGIS integration with sample district boundaries (Pune, Mumbai, Nashik). | ✅ |
| **Vector DB** | `pgvector` enabled; 768-dimension embeddings stored for semantic search. | ✅ |
| **Intelligence** | End-to-end OCR pipeline (Download $\rightarrow$ Tesseract $\rightarrow$ Chunk $\rightarrow$ Embed). | ✅ |
| **Service Layer** | FastAPI serving secure, documented REST APIs with structured JSON logging. | ✅ |

## Looking Ahead (Phase 4: Shared Intelligence)
With the data plumbing, validation, and vectorization layers complete, the platform is now primed for **Phase 4**. The immediate next steps involve building the **Hybrid Search Engine** (combining `pgvector` cosine similarity with PostgreSQL full-text search) and implementing **Retrieval-Augmented Generation (RAG)** pipelines to power the domain-specific intelligence applications (JalSetu, KrishiSetu, etc.).
