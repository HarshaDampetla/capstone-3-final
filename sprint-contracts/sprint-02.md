# Sprint Contract — Sprint 02: Stock Catalog & Watchlist Management

**Sprint Goal:** Stock Catalog CRUD, Soft Delete, & Atomic Watchlists (AC-03, AC-04, AC-05)  
**Business Case:** BC-AINE-006  
**Status:** COMPLETED & VERIFIED  

---

## 1. Scope & Deliverables
- Implement `AC-03`: Admin stock catalog CRUD with mandatory soft delete (`DELETED` status).
- Implement `AC-03`: Customer multi-attribute stock search by symbol, sector, and exchange.
- Implement `AC-04`: Watchlist creation with max 10 limit enforcement.
- Implement `AC-05`: Atomic watchlist updates & deletion (`WatchlistUpdateException`).

---

## 2. Invariants & Acceptance Criteria
- **AC-03 Invariant:** Stocks in `DELETED` status are excluded from customer search results. Hard delete is prohibited.
- **AC-04/05 Invariant:** Watchlist symbol operations are atomic. Exceeding 10 watchlists per customer raises `WatchlistUpdateException`.

---

## 3. Sprint 02 Evaluation & Evidence
- **Tests Passed:** `test_ac_03_admin_stock_crud_api`, `test_ac_04_watchlist_api_creation_and_limit`, `test_ac_05_watchlist_api_atomic_update_and_delete`.
- **Import Linter Status:** 2 contracts kept.
