from src.domain.models import UserRole
from src.domain.exceptions import PermissionDeniedException


class RolePolicy:
    """Domain policy enforcing user role rules and administrative action boundaries (AC-02)."""

    ALLOWED_ROLES = {UserRole.CUSTOMER, UserRole.ADMIN, UserRole.SUSPENDED}

    @classmethod
    def validate_role_transition(cls, actor_role: UserRole, target_role: UserRole) -> None:
        """Only ADMIN actors can update user roles."""
        if actor_role != UserRole.ADMIN:
            raise PermissionDeniedException("Only ADMIN users can update account roles.")
        
        if target_role not in cls.ALLOWED_ROLES:
            raise ValueError(f"Invalid target role: {target_role}")

    @classmethod
    def enforce_admin_access(cls, actor_role: UserRole) -> None:
        """Enforce ADMIN privileges for catalog management and administrative endpoints."""
        if actor_role != UserRole.ADMIN:
            raise PermissionDeniedException("ADMIN role required for this action.")
