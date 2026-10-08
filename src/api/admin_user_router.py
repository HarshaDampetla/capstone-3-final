from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.api.schemas import RoleUpdateRequest, UserResponse
from src.api.dependencies import require_admin
from src.services.user_service import UserService
from src.db.models import UserModel

router = APIRouter(prefix="/api/v1/admin/users", tags=["Admin User Management"])


@router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),
):
    """Admin operation: list all platform users (AC-02)."""
    user_service = UserService(db)
    return user_service.list_users(actor=admin)


@router.put("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    payload: RoleUpdateRequest,
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),
):
    """Admin operation: change a user's role (CUSTOMER, ADMIN, SUSPENDED) with auditing (AC-02)."""
    user_service = UserService(db)
    try:
        updated_user = user_service.update_user_role(
            actor=admin,
            target_user_id=user_id,
            new_role=payload.target_role,
        )
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{user_id}/suspend", response_model=UserResponse)
def suspend_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),
):
    """Admin operation: suspend a user account (AC-02)."""
    user_service = UserService(db)
    try:
        return user_service.suspend_user(actor=admin, target_user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{user_id}/reactivate", response_model=UserResponse)
def reactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),
):
    """Admin operation: reactivate a suspended user account (AC-02)."""
    user_service = UserService(db)
    try:
        return user_service.reactivate_user(actor=admin, target_user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
