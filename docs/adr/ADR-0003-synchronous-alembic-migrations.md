# ADR-0003: Synchronous `psycopg2` for Alembic Migrations in WSL2/Docker

## Status
Accepted

## Context
The runtime FastAPI application uses `asyncpg` for high-concurrency async database operations. However, during local development on WSL2, running Alembic migrations with `asyncpg` resulted in consistent `TimeoutError` exceptions due to WSL2's networking translation layer interacting poorly with `asyncpg`'s strict async connection timeouts.

## Decision
Use the synchronous `psycopg2-binary` driver exclusively for Alembic database migrations, while retaining `asyncpg` for the runtime FastAPI application. The `alembic/env.py` dynamically rewrites the connection string and SSL parameters based on the execution context.

## Consequences
- **Pros:** Eliminates WSL2-specific async networking timeouts. Migrations are inherently synchronous batch operations; async provides no benefit here.
- **Cons:** Requires maintaining two database drivers, but this is an acceptable trade-off for stability and CI/CD reliability.
