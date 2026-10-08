from sqlalchemy.orm import Session
from src.domain.models import PortfolioStats
from src.domain.pnl_calculator import PnLCalculator
from src.repositories.portfolio_repository import PortfolioRepository


class PortfolioService:
    """Service layer calculating portfolio performance metrics (AC-09)."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = PortfolioRepository(db)

    def get_portfolio_stats(self, user_id: int) -> PortfolioStats:
        """Computes customer portfolio metrics using centralized PnLCalculator (AC-09)."""
        holdings = self.repo.get_customer_holdings_with_prices(user_id)
        return PnLCalculator.calculate_portfolio_stats(customer_id=user_id, holdings=holdings)
