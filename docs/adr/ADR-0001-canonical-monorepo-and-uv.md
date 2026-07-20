# ADR-0001: Canonical Monorepo Structure and `uv` Package Management

## Status
Accepted

## Context
Project Sahyadri requires a scalable, maintainable, and strictly typed codebase. Traditional Python tooling (pip, poetry) can be slow and fragmented. We needed a unified approach to dependency management and project structure.

## Decision
1. Adopt a canonical monorepo structure separating `src/`, `tests/`, `docs/`, `docker/`, and `etl/`.
2. Use `uv` (by Astral) as the primary Python package manager and virtual environment handler due to its Rust-based speed and strict lockfile guarantees.
3. Enforce `ruff` for linting/formatting and `mypy` for strict static typing.

## Consequences
- **Pros:** Blazing fast dependency resolution, reproducible builds, and strict adherence to the Sahyadri Engineering Constitution.
- **Cons:** Requires team members to install `uv` instead of relying solely on built-in `pip`.
