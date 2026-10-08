# Watchlist Management Specification
**Feature:** Watchlist Creation, Count Limits (Max 10), & Atomic Operations  
**AC References:** AC-04, AC-05  

---

## 1. Purpose
Define requirements for customer watchlists, including creation with name + symbols, enforcing a maximum limit of 10 watchlists per customer, and atomic updates.

---

## 2. Scope
- Customer watchlist creation (name + at least 1 symbol).
- Maximum 10 watchlists per customer validation.
- Atomic operations (rename, add/remove symbols, delete) raising `WatchlistUpdateException` on partial failures.

---

## 3. Actors
- **Customer:** Authenticated user with `CUSTOMER` role.

---

## 4. User Journeys
1. **Create Watchlist:** Customer submits watchlist name & symbol list → System checks current watchlist count < 10 → Creates watchlist and links symbols atomically → Returns watchlist DTO.
2. **Atomic Update:** Customer submits symbol list update → System executes symbol modification in a single DB transaction → Commits or rolls back entirely with `WatchlistUpdateException`.

---

## 5. Business Rules
- **Rule WL-01:** Watchlist creation MUST specify a non-empty name and at least 1 valid symbol (AC-04).
- **Rule WL-02 (Max 10 Watchlists):** A customer MAY hold a maximum of 10 watchlists. Attempts to create an 11th watchlist MUST raise `WatchlistUpdateException` / HTTP 400 (AC-04).
- **Rule WL-03 (Atomic Operations):** Watchlist operations (rename, add symbol, remove symbol, delete) MUST execute atomically in a single database transaction. Partial updates MUST be rejected with `WatchlistUpdateException` (AC-05).

---

## 6. Domain Model
```python
class WatchlistEntity:
    id: int
    user_id: int
    name: str
    symbols: List[str]
```

---

## 7. API Requirements
- `POST /api/v1/watchlists` — Create new watchlist (max 10 limit).
- `GET /api/v1/watchlists` — List customer watchlists.
- `PUT /api/v1/watchlists/{watchlist_id}` — Rename watchlist or update symbols atomically.
- `DELETE /api/v1/watchlists/{watchlist_id}` — Delete watchlist atomically.

---

## 8. Error Handling
- Creating watchlist when user already holds 10 -> `WatchlistUpdateException` / `400 Bad Request`.
- Creating watchlist with 0 symbols -> `WatchlistUpdateException` / `400 Bad Request`.
- Partial failure during symbol modification -> `WatchlistUpdateException` / `400 Bad Request` (Transaction rolled back).

---

## 9. Security Requirements
- Watchlist operations MUST be partitioned by customer ID (`user_id` from JWT token). Customers cannot view or modify other users' watchlists.

---

## 10. Acceptance Criteria

### AC-04: Watchlist Creation & Max 10 Limit
```gherkin
Given a customer with 9 existing watchlists
When the customer submits a request to create a 10th watchlist named "Tech Growth" with symbol "AAPL"
Then the watchlist is created successfully
When the customer attempts to create an 11th watchlist named "Energy"
Then the request is rejected with a WatchlistUpdateException
And an error response is returned indicating the maximum limit of 10 watchlists has been reached
```

### AC-05: Atomic Watchlist Operations
```gherkin
Given a customer with a watchlist containing symbols ["AAPL", "MSFT"]
When the customer submits an atomic update request adding "NVDA" and removing "AAPL"
Then the operation succeeds and the watchlist symbols become ["MSFT", "NVDA"]
When an invalid symbol or network failure occurs during a partial update
Then the entire operation is rolled back
And a WatchlistUpdateException is raised
And the original watchlist symbols remain unchanged
```

---

## 11. Negative Test Cases
- **NT-WL-01:** Customer with 10 watchlists attempts 11th watchlist creation -> Expect `WatchlistUpdateException`.
- **NT-WL-02:** Submit watchlist creation with empty symbol list `[]` -> Expect `WatchlistUpdateException`.

---

## 12. Non-Functional Requirements
- **NFR-08:** Atomicity enforced via database transaction block and tested in unit suite.

---

## 13. Dependencies
- Depends on `src/domain/watchlist_policy.py`.
