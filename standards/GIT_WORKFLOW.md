# Git Workflow

## Branching Strategy
- `main`: Production-ready code. Protected branch.
- `develop`: Integration branch for features.
- `feature/<name>`: Short-lived branches for new features.
- `hotfix/<name>`: Critical fixes for `main`.

## Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Changes that do not affect the meaning of the code
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `test:` Adding missing tests or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools

Example: `feat(data-atlas): add initial metadata schema for agriculture datasets`
