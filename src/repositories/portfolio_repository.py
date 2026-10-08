from typing import List, Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from src.db.models import PortfolioHoldingModel, StockCatalogModel


class PortfolioRepository:
    """Repository fetching customer portfolio holdings and market quotes (AC-09, AC-10)."""

    def __init__(self, db: Session):
        self.db = db

    def get_customer_holdings_with_prices(self, user_id: int) -> List[Dict[str, Any]]:
        """Retrieves customer holdings merged with latest market price from stock catalog."""
        holdings = self.db.query(PortfolioHoldingModel).filter(PortfolioHoldingModel.user_id == user_id).all()
        result = []

        for h in holdings:
            stock = self.db.query(StockCatalogModel).filter(StockCatalogModel.symbol == h.symbol).first()
            current_price = stock.current_price if stock else h.average_buy_price

            result.append({
                "symbol": h.symbol,
                "quantity": h.quantity,
                "average_buy_price": h.average_buy_price,
                "current_price": current_price,
            })

        return result
