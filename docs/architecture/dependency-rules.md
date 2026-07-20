# Dependency Rules

## Module Boundaries
- `domains` can depend on `core`, `data_atlas`, and `intelligence`.
- `intelligence` can depend on `core` and `data_atlas`.
- `data_atlas` can depend on `core`.
- `core` must not depend on any other internal module.

## Package Naming
- Use lowercase with underscores for package names.
- Avoid circular dependencies.
