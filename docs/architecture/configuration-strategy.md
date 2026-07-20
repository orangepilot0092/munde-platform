# Configuration Strategy

## Environment Variables
- Use `.env` files for local development.
- Use Docker Secrets or Vault for production.

## Pydantic Settings
- All configuration should be managed via Pydantic Settings.
- Validate types and required fields at startup.
