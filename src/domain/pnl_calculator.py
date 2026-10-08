from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any
from src.domain.models import PortfolioStats


class PnLCalculator:
    """Pure domain calculator for portfolio value, P&L, gainers, losers, and sector exposure using Decimal (AC-09, AC-10, NFR-01)."""

    TWO_PLACES = Decimal("0.01")
    FOUR_PLACES = Decimal("0.0001")

    @classmethod
    def validate_decimal_value(cls, val: Any, name: str) -> Decimal:
        """Enforces Python Decimal type and prevents float types or negative values."""
        if isinstance(val, float):
            raise TypeError(f"Financial calculations must use Decimal exclusively (NFR-01). Got float for {name}.")
        
        if not isinstance(val, Decimal):
            try:
                dec_val = Decimal(str(val))
            except Exception:
                raise TypeError(f"Invalid decimal value for {name}: {val}")
        else:
            dec_val = val

        return dec_val

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
            raw_qty = holding["quantity"]
            raw_avg_price = holding["average_buy_price"]
            raw_curr_price = holding["current_price"]

            # Type checking to enforce Decimal only (no float)
            qty = cls.validate_decimal_value(raw_qty, "quantity")
            avg_price = cls.validate_decimal_value(raw_avg_price, "average_buy_price")
            curr_price = cls.validate_decimal_value(raw_curr_price, "current_price")

            if qty < Decimal("0") or avg_price < Decimal("0") or curr_price < Decimal("0"):
                raise ValueError("Holdings quantity and prices cannot be negative values.")

            invested = qty * avg_price
            val = qty * curr_price

            total_invested += invested
            current_value += val

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
            qty = cls.validate_decimal_value(holding["quantity"], "quantity")
            avg_price = cls.validate_decimal_value(holding["average_buy_price"], "average_buy_price")
            curr_price = cls.validate_decimal_value(holding["current_price"], "current_price")

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

    @classmethod
    def calculate_sector_exposure(
        cls,
        holdings: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Calculates value allocation and percentage breakdown per sector using Decimal."""
        sector_totals: Dict[str, Decimal] = {}
        grand_total = Decimal("0.00")

        for holding in holdings:
            sector = holding.get("sector", "General")
            qty = cls.validate_decimal_value(holding["quantity"], "quantity")
            curr_price = cls.validate_decimal_value(holding["current_price"], "current_price")
            val = qty * curr_price

            sector_totals[sector] = sector_totals.get(sector, Decimal("0.00")) + val
            grand_total += val

        exposure = []
        for sector, val in sector_totals.items():
            pct = ((val / grand_total) * Decimal("100")).quantize(cls.TWO_PLACES, rounding=ROUND_HALF_UP) if grand_total > Decimal("0") else Decimal("0.00")
            exposure.append({
                "sector": sector,
                "value": val.quantize(cls.TWO_PLACES, rounding=ROUND_HALF_UP),
                "percentage": pct,
            })

        return sorted(exposure, key=lambda e: e["value"], reverse=True)
