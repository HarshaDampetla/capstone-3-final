from typing import List, Optional
from sqlalchemy.orm import Session
from src.db.models import UserModel
from src.domain.models import UserRole, AccountState
from src.domain.role_rules import RoleManagementRules
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def list_users(self, actor: UserModel) -> List[UserModel]:
        """Admin operation: list all platform users (AC-02)."""
        RoleManagementRules.require_admin_privilege(actor.role)
        return self.user_repo.list_users()

    def update_user_role(self, actor: UserModel, target_user_id: int, new_role: UserRole) -> UserModel:
        """Admin operation: change a user's role with audit logging (AC-02)."""
        RoleManagementRules.validate_role_change(actor.role, new_role)
        
        updated_user = self.user_repo.update_role(
            user_id=target_user_id,
            new_role=new_role,
            actor_id=actor.id,
        )
        if not updated_user:
            raise ValueError(f"User with ID {target_user_id} not found.")

        # If role is set to SUSPENDED, update account state to SUSPENDED as well
        if new_role == UserRole.SUSPENDED:
            updated_user.state = AccountState.SUSPENDED
            self.user_repo.db.commit()
            self.user_repo.db.refresh(updated_user)

        return updated_user

    def suspend_user(self, actor: UserModel, target_user_id: int) -> UserModel:
        """Admin operation: suspend a user account (AC-02)."""
        RoleManagementRules.require_admin_privilege(actor.role)
        return self.update_user_role(actor, target_user_id, UserRole.SUSPENDED)

    def reactivate_user(self, actor: UserModel, target_user_id: int) -> UserModel:
        """Admin operation: reactivate a suspended user account (AC-02)."""
        RoleManagementRules.require_admin_privilege(actor.role)
        user = self.user_repo.get_by_id(target_user_id)
        if not user:
            raise ValueError(f"User with ID {target_user_id} not found.")

        user.state = AccountState.ACTIVE
        user.role = UserRole.CUSTOMER
        self.user_repo.db.commit()
        self.user_repo.db.refresh(user)
        return user
