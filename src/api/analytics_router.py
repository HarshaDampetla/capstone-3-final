from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.db.models import UserModel
from src.api.dependencies import get_current_user
from src.services.analytics_service import AnalyticsService
from src.services.market_data_service import MarketDataService

router = APIRouter(prefix="/api/v1", tags=["Analytics & Market Data"])


@router.get("/analytics/daily")
def get_daily_analytics(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Returns top 5 gainers and top 5 losers from requesting customer's holdings (AC-10)."""
    service = AnalyticsService(db)
    return service.get_customer_daily_analytics(user_id=current_user.id)


@router.get("/analytics/platform")
def get_platform_analytics(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Returns platform-wide order statistics, status volume breakdown, and settlement queue representation."""
    service = AnalyticsService(db)
    return service.get_platform_analytics()


@router.post("/market/tick", status_code=status.HTTP_200_OK)
def trigger_synthetic_price_tick(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """Triggers synthetic random-walk price tick across active stock catalog using Decimal."""
    updated = MarketDataService.tick_stock_prices(db)
    return {
        "status": "success",
        "ticked_stocks_count": len(updated),
        "updates": updated,
    }
