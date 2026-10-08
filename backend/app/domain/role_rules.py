from src.domain.models import UserRole
from src.domain.exceptions import PermissionDeniedException


class RoleManagementRules:
    """Business rules governing admin role updates and permission checks (AC-02, NFR-04)."""

    ALLOWED_ROLES = {UserRole.CUSTOMER, UserRole.ADMIN, UserRole.SUSPENDED}

    @classmethod
    def validate_role_change(cls, actor_role: UserRole, target_role: UserRole) -> None:
        """Enforces that only ADMIN actors can change user roles (AC-02)."""
        if actor_role != UserRole.ADMIN:
            raise PermissionDeniedException("Only ADMIN users can update account roles.")
        
        if target_role not in cls.ALLOWED_ROLES:
            raise ValueError(f"Invalid target role: {target_role}")

    @classmethod
    def require_admin_privilege(cls, actor_role: UserRole) -> None:
        """Enforces ADMIN role requirement for restricted endpoints."""
        if actor_role != UserRole.ADMIN:
            raise PermissionDeniedException("ADMIN role required for this operational endpoint.")
