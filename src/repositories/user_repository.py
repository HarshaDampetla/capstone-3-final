from typing import Optional, List
from sqlalchemy.orm import Session
from src.db.models import UserModel, AuditLogModel
from src.domain.models import UserRole, AccountState


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def create_user(self, email: str, hashed_password: str, role: UserRole = UserRole.CUSTOMER) -> UserModel:
        user = UserModel(
            email=email,
            hashed_password=hashed_password,
            role=role,
            state=AccountState.ACTIVE,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_role(self, user_id: int, new_role: UserRole, actor_id: int) -> Optional[UserModel]:
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        user.role = new_role
        
        # Log audit entry (AC-02)
        audit = AuditLogModel(
            actor_id=actor_id,
            action="UPDATE_USER_ROLE",
            target_user_id=user_id,
            details=f"Role changed to {new_role}",
        )
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_users(self) -> List[UserModel]:
        return self.db.query(UserModel).all()
