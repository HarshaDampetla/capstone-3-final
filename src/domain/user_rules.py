from src.domain.models import UserRole, AccountState
from src.domain.exceptions import DomainException


class UserRegistrationRules:
    """Business rules governing customer registration and initial state (AC-01)."""

    @classmethod
    def validate_new_user(cls, email: str, password: str) -> None:
        if not email or "@" not in email:
            raise ValueError("A valid email address is required for registration.")
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

    @classmethod
    def get_initial_account_state(cls) -> AccountState:
        """New customer accounts must be created in ACTIVE state (AC-01)."""
        return AccountState.ACTIVE

    @classmethod
    def get_initial_user_role(cls) -> UserRole:
        """New accounts default to CUSTOMER role (AC-01)."""
        return UserRole.CUSTOMER
