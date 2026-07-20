# Technical Debt Register

## High Priority
- **Async DB Connections:** Current audit logging uses synchronous DB calls in some paths. Migrate fully to `asyncpg` for non-blocking I/O.
- **Secrets Management:** Currently using `.env` files. Move to Docker Secrets or HashiCorp Vault for production.

## Medium Priority
- **Test Coverage:** Some utility modules (`cache.py`, `rbac.py`) have low test coverage. Add unit tests.
- **Documentation Links:** Some legacy links in `docs/standards/` still point to non-existent files.

## Low Priority
- **Mermaid Diagrams:** Add more detailed sequence diagrams for data ingestion flows.
- **CI/CD Optimization:** Parallelize test jobs in GitHub Actions to reduce build time.
