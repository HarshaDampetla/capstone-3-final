# MarketScope — Domain Rules Mapping & Verification Matrix
**Business Case ID:** BC-AINE-006  
**Domain:** FinTech — Capital Markets / Brokerage  

---

## 1. Overview
This document provides a detailed mapping of every domain business rule across specification files, python policy implementations, and automated test cases.

---

## 2. Domain Rules Mapping Matrix

| Rule ID | Rule Description | Specification File | Implementation Location | Test Location & Tag | Verification Status |
|---|---|---|---|---|---|
| **DR-01** | **User Onboarding & Role Assignment:** New registrations initialize in `ACTIVE` state with `role = CUSTOMER`. | `specs/user-management_spec.md` (AC-01) | `src/domain/user_rules.py` & `src/repositories/user_repository.py` | `tests/unit/test_user_rules.py` (`@pytest.mark.ac("AC-01")`) | **VERIFIED** |
| **DR-02** | **Role Management & Auditing:** Role updates reserved for `ADMIN` role; audited in `audit_logs` with actor ID & timestamp. | `specs/user-management_spec.md` (AC-02) | `src/domain/role_rules.py` & `src/repositories/user_repository.py` | `tests/unit/test_role_rules.py` (`@pytest.mark.ac("AC-02")`) | **VERIFIED** |
| **DR-03** | **Stock Catalog Soft-Delete:** Symbol deletion transitions status to `DELETED`. Hard-deletes strictly prohibited. | `specs/stock-catalog_spec.md` (AC-03) | `src/domain/stock_catalog_rules.py` & `src/repositories/catalog_repository.py` | `tests/unit/test_catalog_rules.py` (`@pytest.mark.ac("AC-03")`) | **VERIFIED** |
| **DR-04** | **Watchlist Count Limit:** Customers hold maximum 10 watchlists. 11th creation throws `WatchlistUpdateException`. | `specs/watchlist_spec.md` (AC-04) | `src/domain/watchlist_rules.py` | `tests/unit/test_watchlist_policy.py` (`@pytest.mark.ac("AC-04")`) | **VERIFIED** |
| **DR-05** | **Atomic Watchlist Updates:** Rename and symbol updates execute atomically or roll back with `WatchlistUpdateException`. | `specs/watchlist_spec.md` (AC-05) | `src/domain/watchlist_rules.py` | `tests/unit/test_watchlist_policy.py` (`@pytest.mark.ac("AC-05")`) | **VERIFIED** |
| **DR-06** | **Order Placement & State Machine:** Orders enter `PENDING` with server timestamp; transition ONLY to `EXECUTED`/`CANCELLED`/`REJECTED`. | `specs/order_spec.md` (AC-06, AC-07) | `src/domain/order_rules.py` | `tests/unit/test_order_policy.py` (`@pytest.mark.ac("AC-07")`) | **VERIFIED** |
| **DR-07** | **Executed Order Immutability:** Orders in `EXECUTED` state cannot be edited or deleted (append-only trade records). | `specs/order_spec.md` (AC-07, NFR-02) | `src/domain/order_rules.py` | `tests/unit/test_order_policy.py` & `.claude/hooks/executed-order-immutability-check.sh` | **VERIFIED** |
| **DR-08** | **BUY Order Funds Check:** BUY order fails with `InsufficientFundsException` if `quote_price × quantity > available_cash`. | `specs/order_spec.md` (AC-08) | `src/domain/funds_validator.py` | `tests/unit/test_funds_validator.py` (`@pytest.mark.ac("AC-08")`) | **VERIFIED** |
| **DR-09** | **Fixed-Point Portfolio P&L:** `total_invested`, `current_value`, `absolute_pnl`, `percent_pnl` computed in `Decimal`. | `specs/portfolio_spec.md` (AC-09) | `src/domain/portfolio_rules.py` & `src/domain/pnl_calculator.py` | `tests/unit/test_pnl_calculator.py` (`@pytest.mark.ac("AC-09")`) | **VERIFIED** |
| **DR-10** | **Daily Gainers & Losers Ranking:** Ranks holdings by percentage P&L and extracts top 5 gainers and top 5 losers. | `specs/analytics_spec.md` (AC-10) | `src/domain/pnl_calculator.py` | `tests/unit/test_pnl_calculator.py` (`@pytest.mark.ac("AC-10")`) | **VERIFIED** |

---

## 3. Automated Rule Verification Commands
- Run domain unit test suite: `pytest tests/unit/ -v`
- Run pre-commit financial and role hooks: `python scripts/run_hooks.py`
