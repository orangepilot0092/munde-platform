# Python Coding Standards

## General Principles
- **Readability:** Code is read more often than it is written. Prioritize clarity.
- **Type Safety:** All functions must have type hints. Use `mypy` for static analysis.
- **Modularity:** Keep functions small and focused. Prefer composition over inheritance.

## Formatting
- Use **Ruff** for formatting and linting.
- Line length: 88 characters.
- Indentation: 4 spaces.

## Imports
- Group imports: Standard library, Third-party, Local.
- Use absolute imports within the `src` package.

## Documentation
- All public modules, classes, and functions must have docstrings (Google Style).
- Update `docs/` whenever code changes affect behavior.
