# Security Standards

## Authentication & Authorization
- Use OAuth2/JWT for API security.
- Implement Role-Based Access Control (RBAC).

## Data Protection
- Encrypt secrets at rest and in transit.
- Never commit secrets to version control.
- Use environment variables or secret managers.

## Input Validation
- Validate all user inputs using Pydantic models.
- Sanitize inputs to prevent SQL injection and XSS.
