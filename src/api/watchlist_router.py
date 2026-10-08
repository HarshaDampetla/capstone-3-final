from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.api.schemas import WatchlistCreateRequest, WatchlistResponse
from src.api.dependencies import get_current_user
from src.services.watchlist_service import WatchlistService
from src.domain.exceptions import WatchlistUpdateException, PermissionDeniedException
from src.db.models import UserModel

router = APIRouter(prefix="/api/v1/watchlists", tags=["Watchlists"])


class WatchlistUpdateRequest(BaseModel):
    name: Optional[str] = None
    symbols: Optional[List[str]] = None


@router.post("", response_model=WatchlistResponse, status_code=status.HTTP_201_CREATED)
def create_watchlist(
    payload: WatchlistCreateRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Customer operation: create new watchlist (AC-04)."""
    service = WatchlistService(db)
    try:
        return service.create_watchlist(
            actor=current_user,
            name=payload.name,
            symbols=payload.symbols,
        )
    except WatchlistUpdateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[WatchlistResponse])
def list_watchlists(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """List authenticated customer's watchlists."""
    service = WatchlistService(db)
    return service.get_customer_watchlists(actor=current_user)


@router.get("/{watchlist_id}", response_model=WatchlistResponse)
def get_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get specific watchlist by ID (enforces ownership)."""
    service = WatchlistService(db)
    try:
        return service.get_watchlist_by_id(actor=current_user, watchlist_id=watchlist_id)
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except WatchlistUpdateException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{watchlist_id}", response_model=WatchlistResponse)
def update_watchlist(
    watchlist_id: int,
    payload: WatchlistUpdateRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Atomically update watchlist name or symbols (AC-05)."""
    service = WatchlistService(db)
    try:
        return service.update_watchlist_atomic(
            actor=current_user,
            watchlist_id=watchlist_id,
            name=payload.name,
            symbols=payload.symbols,
        )
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except WatchlistUpdateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete watchlist atomically (AC-05)."""
    service = WatchlistService(db)
    try:
        service.delete_watchlist(actor=current_user, watchlist_id=watchlist_id)
    except PermissionDeniedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except WatchlistUpdateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
