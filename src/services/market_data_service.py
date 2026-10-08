import random
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from src.db.models import StockCatalogModel
from src.domain.models import StockStatus


class MarketDataService:
    """Synthetic market data service generating random-walk price ticks using Decimal (no real exchange APIs)."""

    @classmethod
    def tick_stock_prices(
        cls,
        db: Session,
        max_tick_percent: Decimal = Decimal("0.02")
    ) -> List[Dict[str, Any]]:
        """Applies a random-walk price tick to active stock catalog items using Decimal arithmetic."""
        stocks = db.query(StockCatalogModel).filter(StockCatalogModel.status == StockStatus.ACTIVE).all()
        updated_stocks = []

        for stock in stocks:
            # Generate deterministic pseudo-random change between -max_tick_percent and +max_tick_percent
            change_factor = Decimal(str(random.uniform(float(-max_tick_percent), float(max_tick_percent))))
            price_delta = (stock.current_price * change_factor).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
            
            new_price = stock.current_price + price_delta
            if new_price < Decimal("0.01"):
                new_price = Decimal("0.01")

            stock.current_price = new_price.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
            stock.updated_at = datetime.now(timezone.utc)

            updated_stocks.append({
                "symbol": stock.symbol,
                "previous_price": stock.current_price - price_delta,
                "current_price": stock.current_price,
                "change_delta": price_delta,
            })

        db.commit()
        return updated_stocks
