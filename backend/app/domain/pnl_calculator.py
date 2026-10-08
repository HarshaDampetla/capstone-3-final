from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any
from src.domain.models import PortfolioStats


class PnLCalculator:
    """Pure domain calculator for portfolio value, P&L, gainers, and losers using Decimal (AC-09, AC-10, NFR-01)."""

    TWO_PLACES = Decimal("0.01")

    @classmethod
    def calculate_portfolio_stats(
        cls,
        customer_id: int,
        holdings: List[Dict[str, Any]]
    ) -> PortfolioStats:
        """Computes total_invested, current_value, absolute_pnl, and percent_pnl using Decimal math (AC-09)."""
        total_invested = Decimal("0.00")
        current_value = Decimal("0.00")

        for holding in holdings:
            qty = Decimal(str(holding["quantity"]))
            avg_price = Decimal(str(holding["average_buy_price"]))
            curr_price = Decimal(str(holding["current_price"]))

            total_invested += qty * avg_price
            current_value += qty * curr_price

        absolute_pnl = current_value - total_invested
        
        if total_invested > Decimal("0"):
            percent_pnl = ((absolute_pnl / total_invested) * Decimal("100")).quantize(cls.TWO_PLACES, rounding=ROUND_HALF_UP)
        else:
            percent_pnl = Decimal("0.00")

        return PortfolioStats(
            customer_id=customer_id,
            total_invested=total_invested.quantize(cls.TWO_PLACES, rounding=ROUND_HALF_UP),
            current_value=current_value.quantize(cls.TWO_PLACES, rounding=ROUND_HALF_UP),
            absolute_pnl=absolute_pnl.quantize(cls.TWO_PLACES, rounding=ROUND_HALF_UP),
            percent_pnl=percent_pnl,
        )

    @classmethod
    def calculate_top_gainers_and_losers(
        cls,
        holdings: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Calculates top 5 gainers and top 5 losers from current customer holdings (AC-10)."""
        scored_holdings = []

        for holding in holdings:
            qty = Decimal(str(holding["quantity"]))
            avg_price = Decimal(str(holding["average_buy_price"]))
            curr_price = Decimal(str(holding["current_price"]))

            if avg_price > Decimal("0"):
                pnl_pct = (((curr_price - avg_price) / avg_price) * Decimal("100")).quantize(cls.TWO_PLACES, rounding=ROUND_HALF_UP)
            else:
                pnl_pct = Decimal("0.00")

            scored_holdings.append({
                "symbol": holding["symbol"],
                "quantity": qty,
                "average_buy_price": avg_price,
                "current_price": curr_price,
                "percent_pnl": pnl_pct,
            })

        sorted_holdings = sorted(scored_holdings, key=lambda h: h["percent_pnl"], reverse=True)

        top_gainers = sorted_holdings[:5]
        top_losers = sorted(sorted_holdings, key=lambda h: h["percent_pnl"])[:5]

        return {
            "top_gainers": top_gainers,
            "top_losers": top_losers,
        }
