# Folder Structure Guide

## src/
- `core/`: Shared platform utilities, config, and logging.
- `data_atlas/`: Metadata registry, connectors, and ETL logic.
- `intelligence/`: AI/ML models, RAG pipelines, and agents.
- `domains/`: Thin application layers (JalSetu, KrishiSetu, etc.).

## tests/
- `unit/`: Isolated component tests.
- `integration/`: Multi-component interaction tests.
- `e2e/`: End-to-end workflow tests.

## docs/
- `architecture/`: System design and infrastructure.
- `standards/`: Engineering and coding guidelines.
- `data-atlas/`: Dataset documentation and schemas.
