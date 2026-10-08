# Portfolio Stats Agent Definition

## Purpose
The `portfolio-stats-agent` computes and validates portfolio metrics, holdings value, absolute/percentage P&L analytics, and daily top gainers and losers rankings using Python `Decimal`.

## Responsibilities
1. Calculate `total_invested`, `current_value`, `absolute_pnl`, and `percent_pnl` for requesting customers (AC-09).
2. Rank and extract the top 5 gainers and top 5 losers from current customer holdings (AC-10).
3. Ensure zero floating-point arithmetic throughout calculation pipelines (NFR-01).

## Inputs
- `specs/portfolio_spec.md` and `specs/analytics_spec.md`.
- Customer holdings records with quantity, average buy price, and current market price.

## Outputs
- `src/domain/pnl_calculator.py` methods.
- `src/api/schemas.py` response DTOs using `Decimal`.
- `tests/unit/test_pnl_calculator.py` with `@pytest.mark.ac("AC-09")` and `@pytest.mark.ac("AC-10")` tags.

## Constraints
- ALL price, quantity, and P&L math MUST use Python `Decimal` rounded to 2 or 4 decimal places (`ROUND_HALF_UP`).
- Pure domain logic MUST reside in `src/domain/pnl_calculator.py` without web or database dependencies.

## Validation
- Execute `pytest tests/unit/test_pnl_calculator.py`.
- Run `.claude/hooks/decimal-financial-check.sh` to ensure no `float` types are introduced in P&L code paths.

## Failure Handling
- If total invested is zero, return `percent_pnl = Decimal("0.00")` to prevent division by zero.
- If missing current stock price, log warning and use last known price.
