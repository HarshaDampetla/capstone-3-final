# Order Placement & Lifecycle Execution Specification
**Feature:** Order Placement, State Machine Lifecycle, Funds Validation, & Immutability  
**AC References:** AC-06, AC-07, AC-08  

---

## 1. Purpose
Define specifications for trade order placement (`BUY`/`SELL`, `MARKET`/`LIMIT`), enforcing the order lifecycle state machine (`PENDING` → `EXECUTED` / `CANCELLED` / `REJECTED`), funds availability verification, and post-execution immutability.

---

## 2. Scope
- Market and Limit `BUY` and `SELL` order placement with server-side timestamping.
- Enforcement of order state machine transitions.
- Validation of customer available cash using Python `Decimal` (`InsufficientFundsException`).
- Post-execution order immutability (append-only trade records).

---

## 3. Actors
- **Customer:** Authenticated user with `CUSTOMER` role placing trade orders.

---

## 4. User Journeys
1. **Order Placement:** Customer submits order payload (symbol, side, order_type, quantity, quote_price) → System verifies funds (for BUY) → Creates order in `PENDING` state with server timestamp → Returns order DTO.
2. **Order Execution:** Evaluator/Service triggers execution → State transitions `PENDING` → `EXECUTED` → Customer available cash and holdings updated atomically.
3. **Order Cancellation:** Customer submits cancel request → System verifies state = `PENDING` → State transitions `PENDING` → `CANCELLED`.

---

## 5. Business Rules
- **Rule ORD-01 (Order Placement):** Customer can place market or limit order (`BUY` or `SELL`). Order MUST enter `PENDING` state with a server-side timestamp (AC-06).
- **Rule ORD-02 (State Machine):** `PENDING` orders MAY transition ONLY to `EXECUTED`, `CANCELLED`, or `REJECTED`. Invalid transitions MUST raise `InvalidOrderStateException` (AC-07).
- **Rule ORD-03 (Immutability):** Orders in `EXECUTED` status ARE IMMUTABLE and append-only. State transitions from `EXECUTED` back to `PENDING` or `CANCELLED` are ILLEGAL (NFR-02, AC-07).
- **Rule ORD-04 (Funds Verification):** For `BUY` orders, total cost `quote_price × quantity` MUST NOT exceed customer's `available_cash`. Arithmetic MUST use Python `Decimal`. If cost exceeds cash, placement MUST fail with `InsufficientFundsException` (AC-08, NFR-01).

---

## 6. Domain Model
```python
class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
```

---

## 7. API Requirements
- `POST /api/v1/orders` — Place market or limit order.
- `GET /api/v1/orders` — List customer orders.
- `DELETE /api/v1/orders/{order_id}` — Cancel pending order.

---

## 8. Error Handling
- Invalid order state transition -> `InvalidOrderStateException` / `400 Bad Request`.
- BUY cost exceeding available cash -> `InsufficientFundsException` / `400 Bad Request`.
- Modifying EXECUTED order -> `InvalidOrderStateException` / `400 Bad Request`.

---

## 9. Security Requirements
- All price, quantity, and cash values MUST be represented as Python `Decimal` in memory and `Numeric(18, 4)` in database. Zero float usage.

---

## 10. Acceptance Criteria

### AC-06: Order Placement
```gherkin
Given a customer with available cash = Decimal("1000.00")
When the customer submits a BUY LIMIT order for "AAPL", quantity = Decimal("2"), quote_price = Decimal("150.00")
Then the order is created in "PENDING" state
And a server-side creation timestamp is assigned
```

### AC-07: Order Lifecycle Enforcement
```gherkin
Given an existing order in "PENDING" state
When the system processes the order execution
Then the order status transitions to "EXECUTED"
When a user attempts to cancel or modify an "EXECUTED" order
Then the action is rejected with an InvalidOrderStateException
And the order status remains "EXECUTED"
```

### AC-08: Insufficient Funds Validation
```gherkin
Given a customer with available cash = Decimal("500.00")
When the customer attempts to place a BUY order for "AAPL", quantity = Decimal("10"), quote_price = Decimal("150.00")
Then the order placement fails
And an InsufficientFundsException is raised indicating required Decimal("1500.00") exceeds available Decimal("500.00")
```

---

## 11. Negative Test Cases
- **NT-ORD-01:** Attempt BUY order exceeding cash -> Expect `InsufficientFundsException`.
- **NT-ORD-02:** Attempt state transition `EXECUTED` -> `CANCELLED` -> Expect `InvalidOrderStateException`.

---

## 12. Non-Functional Requirements
- **NFR-01:** Fixed-Point `Decimal` arithmetic.
- **NFR-02:** Append-only executed trade records.

---

## 13. Dependencies
- Depends on `src/domain/order_policy.py`.
