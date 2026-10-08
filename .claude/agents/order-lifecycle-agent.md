# Order Lifecycle Agent Definition

## Purpose
The `order-lifecycle-agent` is responsible for implementing, validating, and auditing trade order placement, order state machine transitions (`PENDING` → `EXECUTED` / `CANCELLED` / `REJECTED`), funds availability checks, and post-execution order immutability.

## Responsibilities
1. Implement order placement endpoints for `BUY` and `SELL` market or limit orders (AC-06).
2. Validate order state machine transitions and raise `InvalidOrderStateException` on illegal transitions (AC-07).
3. Validate available cash for `BUY` orders using Python `Decimal` and raise `InsufficientFundsException` if cost exceeds cash (AC-08).
4. Enforce post-execution order immutability — executed orders must be append-only (NFR-02).

## Inputs
- `specs/order_spec.md` with explicit Given-When-Then acceptance criteria.
- Customer balance details and quote prices in `Decimal`.
- Existing order state entities.

## Outputs
- `src/domain/order_policy.py` policy methods.
- `src/services/order_service.py` orchestration methods.
- `tests/unit/test_order_policy.py` with `@pytest.mark.ac("AC-06")`, `@pytest.mark.ac("AC-07")`, and `@pytest.mark.ac("AC-08")` tags.

## Constraints
- MUST use Python `Decimal` for all quote prices, quantities, and cash values (NFR-01).
- MUST NEVER allow mutating an order once its status is `EXECUTED` (NFR-02).
- MUST NOT access ORM repositories directly from FastAPI router controllers.

## Validation
- Execute `pytest tests/unit/test_order_policy.py`.
- Run `.claude/hooks/executed-order-immutability-check.sh` to verify immutability.

## Failure Handling
- If an invalid state transition is detected, log the attempt with correlation ID and raise `InvalidOrderStateException`.
- If cash is insufficient, abort the transaction atomically and raise `InsufficientFundsException`.
