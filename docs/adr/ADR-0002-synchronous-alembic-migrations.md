# ADR-0002: Use of Synchronous `psycopg2` for Alembic Migrations

## Status
Accepted

## Context
Project Sahyadri uses `asyncpg` as the primary asynchronous database driver for the FastAPI application to ensure high-concurrency performance. However, during local development on WSL2, running Alembic migrations with `asyncpg` resulted in consistent `TimeoutError` exceptions due to WSL2's networking translation layer interacting poorly with `asyncpg`'s strict async connection timeouts.

## Decision
We will use the synchronous `psycopg2-binary` driver exclusively for Alembic database migrations, while retaining `asyncpg` for the runtime FastAPI application.

## Consequences
### Pros
1. **Reliability:** Eliminates WSL2-specific async networking timeouts during local development and CI/CD pipeline executions.
2. **Simplicity:** Migrations are inherently synchronous, batch operations. Async concurrency provides no benefit here and only adds complexity.
3. **Isolation:** The runtime application's async performance is completely unaffected.

### Cons
1. Requires maintaining two database drivers (`asyncpg` for runtime, `psycopg2-binary` for dev/migrations). This is an acceptable trade-off for stability.

## Compliance
Aligns with the Sahyadri Engineering Principle: *"Simplicity over cleverness"* and *"Design for decades, not sprints."*
