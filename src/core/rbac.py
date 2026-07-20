from fastapi import Depends, HTTPException, status
from typing import List
from src.core.auth import (
    get_current_user,
)  # Assumes get_current_user exists from Sprint 6

# Define Standard Roles
ROLE_ADMIN = "admin"
ROLE_RESEARCHER = "researcher"
ROLE_CITIZEN = "citizen"


class RoleChecker:
    """Dependency class to check user roles against required permissions."""

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")

        # Admins have implicit access to everything
        if user_role == ROLE_ADMIN:
            return current_user

        # Check if user role is in allowed list
        if user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {self.allowed_roles}, Found: {user_role}",
            )
        return current_user


# Pre-configured role checkers for common use cases
require_admin = RoleChecker([ROLE_ADMIN])
require_researcher = RoleChecker([ROLE_ADMIN, ROLE_RESEARCHER])
require_citizen = RoleChecker([ROLE_ADMIN, ROLE_RESEARCHER, ROLE_CITIZEN])
