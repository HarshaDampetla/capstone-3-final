# Analytics Specification
**Feature:** Daily Stock Holdings Analytics, Top Gainers, & Top Losers  
**AC References:** AC-10  

---

## 1. Purpose
Define requirements for daily stock analytics dashboard endpoints, specifically computing the top 5 gainers and top 5 losers from a customer's active holdings.

---

## 2. Scope
- Percentage gain/loss ranking per stock holding.
- Filtering and extraction of top 5 gainers and top 5 losers.

---

## 3. Actors
- **Customer:** Authenticated user with `CUSTOMER` role viewing analytics.

---

## 4. User Journeys
1. **View Daily Analytics:** Customer requests daily analytics → System ranks holdings by percentage P&L → Returns top 5 gainers and top 5 losers.

---

## 5. Business Rules
- **Rule AN-01 (Top Gainers/Losers):** Daily statistics endpoint MUST return top 5 gainers and top 5 losers from requesting customer's holdings (AC-10).
- **Rule AN-02 (Ranking Formula):** Holding gain `% = ((current_price - average_buy_price) / average_buy_price) * 100` calculated in `Decimal`.

---

## 6. Domain Model
```python
class AnalyticsResponse:
    top_gainers: List[HoldingPerformance]
    top_losers: List[HoldingPerformance]
```

---

## 7. API Requirements
- `GET /api/v1/analytics/daily` — Returns top 5 gainers and top 5 losers from customer holdings.

---

## 8. Error Handling
- Customer with fewer than 5 holdings -> Returns available holdings sorted accordingly.

---

## 9. Security Requirements
- Analytics MUST be scoped strictly to requesting customer ID.

---

## 10. Acceptance Criteria

### AC-10: Daily Top Gainers & Losers Ranking
```gherkin
Given a customer holding stocks "WINNER" (gain = +50.00%), "NEUTRAL" (gain = 0.00%), and "LOSER" (gain = -50.00%)
When the customer requests daily statistics from "GET /api/v1/analytics/daily"
Then top_gainers includes "WINNER" at rank 1
And top_losers includes "LOSER" at rank 1
And results are computed using Python Decimal arithmetic
```

---

## 11. Negative Test Cases
- **NT-AN-01:** Customer with 0 holdings requests daily analytics -> Returns empty lists `{"top_gainers": [], "top_losers": []}`.

---

## 12. Non-Functional Requirements
- **NFR-01:** Fixed-Point `Decimal` arithmetic.

---

## 13. Dependencies
- Depends on `src/domain/pnl_calculator.py`.
