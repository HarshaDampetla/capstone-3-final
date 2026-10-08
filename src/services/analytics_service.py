from typing import Dict, Any, List
from decimal import Decimal
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.db.models import OrderModel, StockCatalogModel, PortfolioHoldingModel
from src.domain.models import OrderStatus
from src.domain.pnl_calculator import PnLCalculator
from src.repositories.portfolio_repository import PortfolioRepository


class AnalyticsService:
    """Service layer aggregating customer holdings analytics and platform trading metrics (AC-10)."""

    def __init__(self, db: Session):
        self.db = db
        self.portfolio_repo = PortfolioRepository(db)

    def get_customer_daily_analytics(self, user_id: int) -> Dict[str, Any]:
        """Returns top 5 gainers, top 5 losers, sector exposure, and portfolio stats for requested customer (AC-10)."""
        holdings = self.portfolio_repo.get_customer_holdings_with_prices(user_id)

        # Scoped strictly to requesting customer ID
        gainers_losers = PnLCalculator.calculate_top_gainers_and_losers(holdings)
        sector_exposure = PnLCalculator.calculate_sector_exposure(holdings)
        stats = PnLCalculator.calculate_portfolio_stats(customer_id=user_id, holdings=holdings)

        return {
            "top_gainers": gainers_losers["top_gainers"],
            "top_losers": gainers_losers["top_losers"],
            "sector_exposure": sector_exposure,
            "portfolio_stats": {
                "total_invested": stats.total_invested,
                "current_value": stats.current_value,
                "absolute_pnl": stats.absolute_pnl,
                "percent_pnl": stats.percent_pnl,
            }
        }

    def get_platform_analytics(self) -> Dict[str, Any]:
        """Calculates platform-wide trade volume, status breakdown, top traded stocks, and settlement queue."""
        total_orders = self.db.query(OrderModel).count()
        
        # Order volume by status
        volume_by_status = {}
        for status_enum in OrderStatus:
            count = self.db.query(OrderModel).filter(OrderModel.status == status_enum).count()
            volume_by_status[status_enum.value] = count

        # Settlement Queue (Pending orders awaiting execution/settlement)
        pending_orders = (
            self.db.query(OrderModel)
            .filter(OrderModel.status == OrderStatus.PENDING)
            .order_by(OrderModel.created_at.asc())
            .all()
        )
        settlement_queue = [
            {
                "order_id": o.id,
                "user_id": o.user_id,
                "symbol": o.symbol,
                "side": o.side.value,
                "order_type": o.order_type.value,
                "quantity": o.quantity,
                "quote_price": o.quote_price,
                "status": o.status.value,
                "created_at": o.created_at,
            }
            for o in pending_orders
        ]

        # Most traded symbols
        most_traded = (
            self.db.query(OrderModel.symbol, func.count(OrderModel.id).label("trade_count"))
            .group_by(OrderModel.symbol)
            .order_by(func.count(OrderModel.id).desc())
            .limit(5)
            .all()
        )
        most_traded_list = [{"symbol": item[0], "trade_count": item[1]} for item in most_traded]

        return {
            "total_orders": total_orders,
            "volume_by_status": volume_by_status,
            "most_traded_symbols": most_traded_list,
            "settlement_queue_length": len(settlement_queue),
            "settlement_queue": settlement_queue,
        }
