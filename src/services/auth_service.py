from typing import Optional, Tuple
from sqlalchemy.orm import Session
from src.core.security import get_password_hash, verify_password, create_access_token
from src.db.models import UserModel
from src.domain.user_rules import UserRegistrationRules
from src.domain.models import UserRole, AccountState
from src.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_customer(self, email: str, password: str) -> UserModel:
        """Customer registration implementation (AC-01)."""
        # Domain validation
        UserRegistrationRules.validate_new_user(email, password)
        
        # Check duplicate
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError(f"Email '{email}' is already registered.")

        # Hash password securely via bcrypt (NFR-03)
        hashed_password = get_password_hash(password)
        
        # Create user in ACTIVE state with role = CUSTOMER (AC-01)
        user = self.user_repo.create_user(
            email=email,
            hashed_password=hashed_password,
            role=UserRegistrationRules.get_initial_user_role(),
        )
        return user

    def authenticate_user(self, email: str, password: str) -> Tuple[UserModel, str]:
        """Authenticate user credentials and return JWT access token."""
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password credentials.")

        if user.state == AccountState.SUSPENDED or user.role == UserRole.SUSPENDED:
            raise ValueError("Account is suspended.")

        token = create_access_token(subject=user.id, role=user.role.value)
        return user, token
