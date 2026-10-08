from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any


class PortfolioRules:
    """Business rules governing portfolio performance metrics and gainers/losers ranking (AC-09, AC-10)."""

    TWO_DECIMALS = Decimal("0.01")

    @classmethod
    def calculate_metrics(
        cls,
        holdings: List[Dict[str, Any]]
    ) -> Dict[str, Decimal]:
        """Calculates total_invested, current_value, absolute_pnl, and percent_pnl using Decimal (AC-09)."""
        total_invested = Decimal("0.00")
        current_value = Decimal("0.00")

        for h in holdings:
            qty = Decimal(str(h["quantity"]))
            avg_price = Decimal(str(h["average_buy_price"]))
            curr_price = Decimal(str(h["current_price"]))

            total_invested += qty * avg_price
            current_value += qty * curr_price

        abs_pnl = current_value - total_invested
        if total_invested > Decimal("0"):
            pct_pnl = ((abs_pnl / total_invested) * Decimal("100")).quantize(cls.TWO_DECIMALS, rounding=ROUND_HALF_UP)
        else:
            pct_pnl = Decimal("0.00")

        return {
            "total_invested": total_invested.quantize(cls.TWO_DECIMALS, rounding=ROUND_HALF_UP),
            "current_value": current_value.quantize(cls.TWO_DECIMALS, rounding=ROUND_HALF_UP),
            "absolute_pnl": abs_pnl.quantize(cls.TWO_DECIMALS, rounding=ROUND_HALF_UP),
            "percent_pnl": pct_pnl,
        }
