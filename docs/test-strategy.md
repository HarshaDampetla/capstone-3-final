# MarketScope — Comprehensive Test Strategy & Evidence Report

**Business Case ID:** BC-AINE-006  
**Domain:** FinTech — Capital Markets / Brokerage  
**Test Framework:** `pytest` + `pytest-cov` + `import-linter`  

---

## 1. Executive Summary
The MarketScope platform enforces a specification-driven, automated test strategy across all architectural layers. Every functional requirement (AC-01 through AC-10) is backed by explicit pytest markers, domain invariant checks, and architectural boundary linting.

---

## 2. Test Pyramid & Directory Structure

```
tests/ (and backend/tests/)
├── architecture/
│   └── test_layering.py            # Layer isolation, zero external domain imports, AST float scan
├── integration/
│   ├── test_analytics_api.py       # Daily top 5 gainers/losers (AC-10) & platform stats
│   ├── test_order_api.py           # Order placement, execution, immutability & funds (AC-06..08)
│   ├── test_portfolio_api.py       # Portfolio performance metrics (AC-09)
│   ├── test_stock_catalog.py       # Admin stock CRUD & customer search (AC-03)
│   ├── test_user_management.py     # Auth, role changes & account state checks (AC-01..02)
│   └── test_watchlist_api.py       # Watchlist creation, limit 10 & atomic rollback (AC-04..05)
└── unit/
    ├── test_auth.py                # Password hashing, JWT token creation & role verification
    ├── test_catalog.py             # Stock catalog domain rules & soft delete
    ├── test_domain_rules.py        # Domain business logic validators
    ├── test_order_policy.py        # Order state machine & funds validation
    ├── test_pnl_calculator.py      # Portfolio P&L, gainers/losers, sector exposure & Decimal math
    ├── test_watchlist.py           # Watchlist domain invariants & ownership isolation
    └── test_watchlist_policy.py    # Max 10 limit & symbol cleaning
```

---

## 3. Test Categories & Verification Coverage

| Category | Count | Focus Areas | Governing Rules |
|---|---|---|---|
| **1. Unit Tests** | 24 | Pure domain logic, PnL math, state machine policies | NFR-01, NFR-02 |
| **2. Integration Tests** | 19 | API endpoints, DB transaction rollbacks, ownership isolation | AC-01 to AC-10 |
| **3. API Tests** | 19 | FastAPI endpoints, status codes (201, 200, 400, 403, 404, 422) | HTTP Contracts |
| **4. Authorization Tests** | 6 | CUSTOMER vs ADMIN role partitioning, suspended user block | NFR-04 |
| **5. Domain Rule Tests** | 8 | Positive price/quantity validation, soft delete invariants | Domain Invariants |
| **6. Financial Calculation Tests** | 7 | Profit, loss, zero investment, fractional qty, AST zero float scan | NFR-01 |
| **7. Architecture Tests** | 4 | Domain isolation, controller repository isolation, AST float check | ARCH-01 |
| **8. AC Traceability Tests** | 10 | Explicit `@pytest.mark.ac("AC-NN")` markers for AC-01 to AC-10 | AC Traceability |

---

## 4. Financial Precision & AST Zero-Float Guarantee (NFR-01)
- **Decimal Invariant:** All financial values (`quote_price`, `quantity`, `available_cash`, `total_invested`, `current_value`, `absolute_pnl`, `percent_pnl`) use Python `Decimal`.
- **AST Architecture Check:** `test_financial_calculations_never_use_float_ast` parses the Abstract Syntax Tree of all domain financial modules (`pnl_calculator.py`, `funds_validator.py`, `order_policy.py`) to guarantee zero `float` literals or `float()` calls exist in production domain code.

---

## 5. Empirical Verification & Coverage Metrics

```bash
======================= 51 passed, 1 warning in 17.21s ========================
TOTAL Statement Coverage: 86% (Required: >= 80%)
Coverage XML Written: coverage.xml
Import Linter Contracts: 2 KEPT, 0 BROKEN
```

| Component | Statements | Missed | Coverage |
|---|---|---|---|
| `src/domain/pnl_calculator.py` | 70 | 5 | **93%** |
| `src/services/analytics_service.py` | 29 | 0 | **100%** |
| `src/services/market_data_service.py` | 23 | 1 | **96%** |
| `src/repositories/portfolio_repository.py` | 15 | 0 | **100%** |
| `src/services/portfolio_service.py` | 11 | 0 | **100%** |
| `src/api/portfolio_router.py` | 13 | 0 | **100%** |
| `src/api/analytics_router.py` | 21 | 0 | **100%** |
| `src/db/models.py` | 75 | 0 | **100%** |
| **TOTAL** | **1330** | **189** | **86%** |
