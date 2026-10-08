from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.db.models import UserModel
from src.api.dependencies import get_current_user
from src.api.schemas import PortfolioStatsResponse
from src.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/api/v1/portfolio", tags=["Portfolio"])


@router.get("/stats", response_model=PortfolioStatsResponse)
def get_portfolio_stats(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns portfolio performance metrics (total_invested, current_value, absolute_pnl, percent_pnl) (AC-09)."""
    service = PortfolioService(db)
    stats = service.get_portfolio_stats(current_user.id)
    return PortfolioStatsResponse(
        customer_id=stats.customer_id,
        total_invested=stats.total_invested,
        current_value=stats.current_value,
        absolute_pnl=stats.absolute_pnl,
        percent_pnl=stats.percent_pnl,
    )
