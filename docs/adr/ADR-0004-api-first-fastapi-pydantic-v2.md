# ADR-0004: API-First Design with FastAPI, Pydantic V2, and Async Runtime

## Status
Accepted

## Context
Sahyadri must expose its Intelligence Assets via a secure, self-documenting, and high-performance API. 

## Decision
1. Use **FastAPI** as the web framework for its native async support and automatic OpenAPI/Swagger generation.
2. Use **Pydantic V2** for strict data validation and serialization, utilizing the `model_config = {"from_attributes": True}` pattern to seamlessly map SQLAlchemy models to API responses.
3. Implement a dependency-injected `AsyncSession` for database interactions to ensure non-blocking I/O.

## Consequences
- **Pros:** Self-documenting APIs, strict type safety at runtime, and high throughput.
- **Cons:** Requires developers to understand async/await patterns and Pydantic V2 syntax.
