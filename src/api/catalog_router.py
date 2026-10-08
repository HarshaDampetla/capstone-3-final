from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.api.schemas import StockCreateRequest, StockUpdateRequest, StockResponse
from src.api.dependencies import get_current_user, require_admin
from src.services.catalog_service import CatalogService
from src.db.models import UserModel

public_router = APIRouter(prefix="/api/v1/catalog", tags=["Stock Catalog"])
admin_router = APIRouter(prefix="/api/v1/admin/catalog", tags=["Admin Stock Catalog"])


# Customer / Public Catalog Endpoints
@public_router.get("", response_model=List[StockResponse])
def browse_stocks(
    symbol: Optional[str] = Query(None, description="Search by stock symbol"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    exchange: Optional[str] = Query(None, description="Filter by exchange"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Browse active stock catalog with optional symbol, sector, or exchange search filters (AC-03)."""
    service = CatalogService(db)
    return service.search_stocks(symbol=symbol, sector=sector, exchange=exchange)


@public_router.get("/{symbol}", response_model=StockResponse)
def get_stock(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Get stock details by symbol (AC-03)."""
    service = CatalogService(db)
    try:
        return service.get_stock_by_symbol(symbol)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Admin Catalog Management Endpoints
@admin_router.post("", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
def create_stock(
    payload: StockCreateRequest,
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),
):
    """Admin operation: create new stock symbol (AC-03)."""
    service = CatalogService(db)
    try:
        return service.create_stock(
            actor=admin,
            symbol=payload.symbol,
            company_name=payload.company_name,
            sector=payload.sector,
            exchange=payload.exchange,
            current_price=payload.current_price,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@admin_router.put("/{symbol}", response_model=StockResponse)
def update_stock(
    symbol: str,
    payload: StockUpdateRequest,
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),
):
    """Admin operation: update stock symbol details (AC-03)."""
    service = CatalogService(db)
    try:
        return service.update_stock(
            actor=admin,
            symbol=symbol,
            company_name=payload.company_name,
            sector=payload.sector,
            exchange=payload.exchange,
            current_price=payload.current_price,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@admin_router.delete("/{symbol}", response_model=StockResponse)
def soft_delete_stock(
    symbol: str,
    db: Session = Depends(get_db),
    admin: UserModel = Depends(require_admin),
):
    """Admin operation: soft-delete stock symbol to DELETED state (AC-03). Symbols are never hard deleted."""
    service = CatalogService(db)
    try:
        return service.soft_delete_stock(actor=admin, symbol=symbol)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
