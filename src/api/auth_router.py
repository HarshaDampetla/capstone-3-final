from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.api.schemas import UserRegisterRequest, UserResponse
from src.services.auth_service import AuthService
from src.api.dependencies import get_current_user
from src.db.models import UserModel

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_customer(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    """Customer Registration Endpoint (AC-01).

    Registers new customer account in ACTIVE state with role = CUSTOMER.
    Password is securely hashed via bcrypt. Plaintext password is never logged or returned.
    """
    auth_service = AuthService(db)
    try:
        user = auth_service.register_customer(payload.email, payload.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """User Login Endpoint. Authenticates credentials and returns JWT Bearer token."""
    auth_service = AuthService(db)
    try:
        user, token = auth_service.authenticate_user(payload.email, payload.password)
        return TokenResponse(access_token=token, user=user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserModel = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user
