# Sprint Contract — Sprint 03: Trading Engine, Analytics, & UI Integration

**Sprint Goal:** Order Placement, State Machine, Portfolio Stats, Daily Analytics & Playwright UI (AC-06 to AC-10)  
**Business Case:** BC-AINE-006  
**Status:** COMPLETED & VERIFIED  

---

## 1. Scope & Deliverables
- Implement `AC-06`: Market/Limit `BUY`/`SELL` order placement with server-side UTC timestamping.
- Implement `AC-07`: Order state machine (`PENDING` → `EXECUTED`/`CANCELLED`/`REJECTED`) & executed order immutability (NFR-02).
- Implement `AC-08`: Insufficient funds validation (`quote_price * quantity > available_cash` raises `InsufficientFundsException`).
- Implement `AC-09`: Portfolio performance metrics (`total_invested`, `current_value`, `absolute_pnl`, `percent_pnl`) using Python `Decimal`.
- Implement `AC-10`: Daily top 5 gainers & top 5 losers ranking from customer holdings.
- Implement React TypeScript Frontend & Playwright E2E UI Validation suite.

---

## 2. Invariants & Acceptance Criteria
- **Fixed-Point Financial Policy (NFR-01):** `Decimal` arithmetic exclusively. Float types prohibited across domain code.
- **Append-Only Immutability (NFR-02):** Executed trade records cannot be modified or deleted.

---

## 3. Sprint 03 Evaluation & Evidence
- **Pytest Suite:** 54/54 passed (100% pass rate, 86% statement coverage).
- **Playwright Suite:** 10/10 E2E browser scenarios passed.
- **Import Linter:** 2 contracts kept, 0 broken.
