# Portfolio Statistics Specification
**Feature:** Customer Portfolio Metrics, Holdings Valuation, & P&L Analysis  
**AC References:** AC-09  

---

## 1. Purpose
Define requirements for computing customer portfolio performance metrics, including total invested capital, current market value, absolute P&L, and percentage P&L using Python `Decimal`.

---

## 2. Scope
- Calculation of portfolio holdings value based on average buy price and current market prices.
- Computation of `total_invested`, `current_value`, `absolute_pnl`, and `percent_pnl` metrics.
- Decimal math precision and rounding standards.

---

## 3. Actors
- **Customer:** Authenticated user with `CUSTOMER` role viewing portfolio stats.

---

## 4. User Journeys
1. **View Portfolio Stats:** Customer requests portfolio summary → System retrieves customer holdings and current stock prices → Computes metrics using Decimal math → Returns portfolio stats DTO.

---

## 5. Business Rules
- **Rule PF-01 (Portfolio Metrics):** Portfolio statistics endpoint MUST return `total_invested`, `current_value`, `absolute_pnl`, and `percent_pnl` for requesting customer (AC-09).
- **Rule PF-02 (Decimal Computation):** All metric calculations MUST use Python `Decimal` rounded to 2 decimal places (`ROUND_HALF_UP`) (NFR-01).
- **Rule PF-03 (P&L Formulas):**
  - `total_invested = sum(quantity * average_buy_price)`
  - `current_value = sum(quantity * current_price)`
  - `absolute_pnl = current_value - total_invested`
  - `percent_pnl = (absolute_pnl / total_invested) * 100` (if total_invested > 0 else 0.00).

---

## 6. Domain Model
```python
@dataclass
class PortfolioStats:
    customer_id: int
    total_invested: Decimal
    current_value: Decimal
    absolute_pnl: Decimal
    percent_pnl: Decimal
```

---

## 7. API Requirements
- `GET /api/v1/portfolio/stats` — Returns portfolio statistics for authenticated customer.

---

## 8. Error Handling
- Customer with 0 holdings -> Returns all metrics as `Decimal("0.00")`.

---

## 9. Security Requirements
- Portfolio statistics MUST be scoped to requesting customer ID from JWT claims.

---

## 10. Acceptance Criteria

### AC-09: Portfolio Performance Metrics
```gherkin
Given a requesting customer holding 10 shares of "AAPL" (buy price = Decimal("150.00"), current price = Decimal("180.00"))
And 5 shares of "MSFT" (buy price = Decimal("300.00"), current price = Decimal("280.00"))
When the customer requests portfolio statistics from "GET /api/v1/portfolio/stats"
Then the endpoint returns total_invested = Decimal("3000.00")
And current_value = Decimal("3200.00")
And absolute_pnl = Decimal("200.00")
And percent_pnl = Decimal("6.67")
And all returned numeric values are represented as Python Decimal
```

---

## 11. Negative Test Cases
- **NT-PF-01:** Customer with 0 holdings requests stats -> Expect all zero Decimals without DivisionByZero error.

---

## 12. Non-Functional Requirements
- **NFR-01:** Fixed-Point `Decimal` arithmetic.

---

## 13. Dependencies
- Depends on `src/domain/pnl_calculator.py`.
