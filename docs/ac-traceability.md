# MarketScope — Acceptance Criteria Traceability Matrix
**Business Case ID:** BC-AINE-006  
**Domain:** FinTech — Capital Markets / Brokerage  

---

## 1. Overview
This matrix provides end-to-end traceability mapping every official Acceptance Criterion (`AC-01` through `AC-10`) from its governing specification file, through domain policies and service implementation locations, to unit and integration test cases with empirical evidence artifacts.

---

## 2. Complete Traceability Matrix

| AC ID | Description | Spec Location | Implementation Location | Test Location & Tag | Evidence Artifact | Status |
|---|---|---|---|---|---|---|
| **AC-01** | Customer registration (`ACTIVE` state, `CUSTOMER` role, bcrypt hash) | `specs/user-management_spec.md` | `src/repositories/user_repository.py`<br>`src/core/security.py` | `tests/unit/test_auth.py`<br>`tests/integration/test_user_management.py`<br>(`@pytest.mark.ac("AC-01")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-02** | Admin role management & auditing (`CUSTOMER`/`ADMIN`/`SUSPENDED`) | `specs/user-management_spec.md` | `src/domain/role_policy.py`<br>`src/repositories/user_repository.py` | `tests/unit/test_auth.py`<br>`tests/integration/test_user_management.py`<br>(`@pytest.mark.ac("AC-02")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-03** | Stock catalog CRUD & soft delete (`DELETED` status, never hard-deleted) | `specs/stock-catalog_spec.md` | `src/repositories/catalog_repository.py` | `tests/unit/test_catalog.py`<br>`tests/integration/test_stock_catalog.py`<br>(`@pytest.mark.ac("AC-03")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-04** | Watchlist creation with name + >= 1 symbol; max 10 watchlists per user | `specs/watchlist_spec.md` | `src/domain/watchlist_policy.py`<br>`src/services/watchlist_service.py` | `tests/unit/test_watchlist_policy.py`<br>`tests/integration/test_watchlist_api.py`<br>(`@pytest.mark.ac("AC-04")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-05** | Atomic watchlist operations (`WatchlistUpdateException` on partial failure) | `specs/watchlist_spec.md` | `src/domain/watchlist_policy.py`<br>`src/repositories/watchlist_repository.py` | `tests/unit/test_watchlist.py`<br>`tests/integration/test_watchlist_api.py`<br>(`@pytest.mark.ac("AC-05")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-06** | Market/Limit BUY/SELL order placement (`PENDING` state + server timestamp) | `specs/order_spec.md` | `src/domain/order_policy.py`<br>`src/services/order_service.py` | `tests/integration/test_order_api.py`<br>(`@pytest.mark.ac("AC-06")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-07** | Order state machine (`PENDING` → `EXECUTED`/`CANCELLED`/`REJECTED`, immutability) | `specs/order_spec.md` | `src/domain/order_policy.py`<br>`src/domain/order_rules.py` | `tests/unit/test_order_policy.py`<br>`tests/integration/test_order_api.py`<br>(`@pytest.mark.ac("AC-07")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-08** | Insufficient funds check (`BUY` total cost > cash raises `InsufficientFundsException`) | `specs/order_spec.md` | `src/domain/funds_validator.py`<br>`src/domain/order_policy.py` | `tests/unit/test_order_policy.py`<br>`tests/integration/test_order_api.py`<br>(`@pytest.mark.ac("AC-08")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-09** | Portfolio statistics (`total_invested`, `current_value`, `absolute_pnl`, `percent_pnl`) | `specs/portfolio_spec.md` | `src/domain/pnl_calculator.py`<br>`src/services/portfolio_service.py` | `tests/unit/test_pnl_calculator.py`<br>`tests/integration/test_portfolio_api.py`<br>(`@pytest.mark.ac("AC-09")`) | `coverage.xml` & `pytest` output | **VERIFIED** |
| **AC-10** | Daily statistics (top 5 gainers & top 5 losers from current holdings) | `specs/analytics_spec.md` | `src/domain/pnl_calculator.py`<br>`src/services/analytics_service.py` | `tests/unit/test_pnl_calculator.py`<br>`tests/integration/test_analytics_api.py`<br>(`@pytest.mark.ac("AC-10")`) | `coverage.xml` & `pytest` output | **VERIFIED** |

---

## 3. Specification Review & Audit
All 7 specification files (`app_spec.md`, `user-management_spec.md`, `stock-catalog_spec.md`, `watchlist_spec.md`, `order_spec.md`, `portfolio_spec.md`, `analytics_spec.md`) have been verified against implementation code and test suites:
- **Zero Contradictions Found:** Role names (`CUSTOMER`, `ADMIN`, `SUSPENDED`), Order statuses (`PENDING`, `EXECUTED`, `CANCELLED`, `REJECTED`), and Stock statuses (`ACTIVE`, `DELETED`, `DELISTED`) are 100% aligned across all specs.
- **Fixed-Point Financial Invariant:** Every spec mandates `Decimal` for financial values without exception.
- **Verification Coverage:** 100% of acceptance criteria (AC-01 to AC-10) are verified by passing automated unit/integration tests with 86% total backend statement coverage.
