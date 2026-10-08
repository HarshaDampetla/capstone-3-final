---
name: portfolio-pnl-calculator
description: Calculates total_invested, current_value, absolute_pnl, percent_pnl, and top 5 gainers/losers using Decimal.
---

# Portfolio PnL Calculator Skill

## Purpose & Usage
Use this skill when implementing portfolio statistics endpoints or daily gainers and losers rankings (AC-09, AC-10).

## Mathematical Invariants & Rules

1. **Exact Decimal Computations (NFR-01, AC-09):**
   - `total_invested = sum(Decimal(qty) * Decimal(avg_buy_price))`
   - `current_value = sum(Decimal(qty) * Decimal(current_price))`
   - `absolute_pnl = current_value - total_invested`
   - `percent_pnl = ((absolute_pnl / total_invested) * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` (if `total_invested > 0` else `Decimal("0.00")`).

2. **Gainers & Losers Ranking (AC-10):**
   - Calculate individual holding `percent_pnl = (((current_price - avg_price) / avg_price) * Decimal("100"))`.
   - Sort descending for Top 5 Gainers; sort ascending for Top 5 Losers.

## Verification Command
```bash
pytest tests/unit/test_pnl_calculator.py -v
```
