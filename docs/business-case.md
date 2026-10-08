# MarketScope — Business Case & Domain Documentation
**Business Case ID:** BC-AINE-006  
**Domain:** FinTech — Capital Markets / Brokerage  
**Project Type:** AI-Native Engineering Capstone  

---

## 1. Problem Statement
Retail brokerages struggle to provide modern, self-serve trading and portfolio analytics platforms that guarantee role boundary isolation, order execution immutability, and fixed-point precision math. Legacy trading systems often suffer from floating-point rounding errors in P&L reporting, mutable execution logs leading to audit failures, and complex onboarding workflows. MarketScope solves these challenges by delivering an auditable, self-serve trading platform with strict domain boundaries and automated AI-native substrate guardrails.

---

## 2. Target Users
1. **Retail Customer (Trader):** Self-serve user onboarded to trade stocks, construct custom watchlists, monitor current holdings, and inspect daily portfolio P&L analytics.
2. **Brokerage Administrator (Admin):** Compliance and system manager responsible for user account state auditing, role assignment (`CUSTOMER`, `ADMIN`, `SUSPENDED`), and stock catalog lifecycle administration.
3. **Automated Auditor / Evaluator:** AI-native evaluator and CI pipeline verifying specs, domain rules, and security guardrails.

---

## 3. Customer User Journeys
- **Journey 1 — Self-Onboarding:** Customer registers with email & password → Account initialized in `ACTIVE` state with `role = CUSTOMER` → Obtains JWT access token.
- **Journey 2 — Stock Discovery & Watchlist Management:** Customer searches stock catalog → Constructs custom named watchlists (at least 1 symbol, max 10 watchlists) → Modifies watchlist symbols atomically.
- **Journey 3 — Trade Order Placement:** Customer inspects cash balance → Places Market or Limit BUY/SELL order → Order enters `PENDING` state with server timestamp → Order executes or cancels.
- **Journey 4 — Portfolio Performance & Daily Analytics:** Customer opens dashboard → Inspects `total_invested`, `current_value`, `absolute_pnl`, `percent_pnl` → Views Top 5 Gainers and Top 5 Losers.

---

## 4. Admin User Journeys
- **Journey 1 — User Role & Account Administration:** Admin lists accounts → Updates user role (`CUSTOMER`, `ADMIN`, `SUSPENDED`) → Action is recorded in `audit_logs` with actor ID and server timestamp.
- **Journey 2 — Stock Catalog Lifecycle Management:** Admin creates stock symbol → Updates price → Soft-deletes symbol (`DELETED` status). Symbols are never hard-deleted.

---

## 5. Business Value Proposition
- **Auditability & Integrity:** Append-only executed order records and audit logs ensure 100% regulatory compliance.
- **Financial Accuracy:** Fixed-point `Decimal` math eliminates floating-point rounding errors in P&L and available cash.
- **Self-Serve Efficiency:** Automated customer registration, watchlist management, and instant analytics reduce operational overhead.

---

## 6. Key Success Metrics
- **Functional Compliance:** 100% pass rate across all 10 Acceptance Criteria (`AC-01` to `AC-10`).
- **Precision Integrity:** Zero floating-point operations in financial calculation code paths (NFR-01).
- **Latency & Performance:** `/health` endpoint responds within 1 second of startup (NFR-07).
- **Architectural Discipline:** Zero cross-layer violations detected by `import-linter` (ARCH-02).

---

## 7. Domain Rules & Trading Constraints
- **Rule BR-01 (Role Partitioning):** Admin endpoints are strictly isolated from Customer role access (NFR-04).
- **Rule BR-02 (Watchlist Limit):** Maximum 10 watchlists per customer (AC-04).
- **Rule BR-03 (Watchlist Atomicity):** Watchlist updates execute atomically; partial updates raise `WatchlistUpdateException` (AC-05).
- **Rule BR-04 (Order State Machine):** `PENDING` → `EXECUTED` / `CANCELLED` / `REJECTED`. Executed orders are immutable (AC-07, NFR-02).
- **Rule BR-05 (BUY Funds Check):** BUY orders fail if `quote_price × quantity > available_cash` (`InsufficientFundsException`, AC-08).
- **Rule BR-06 (Catalog Soft Delete):** Symbol deletion transitions status to `DELETED`. Hard-deletes are forbidden (AC-03).

---

## 8. Portfolio Analytics Specifications
- **Portfolio Stats (AC-09):** Computes `total_invested`, `current_value`, `absolute_pnl`, and `percent_pnl` using Python `Decimal` (`ROUND_HALF_UP`).
- **Daily Analytics (AC-10):** Ranks holdings by percentage P&L and returns top 5 gainers and top 5 losers.

---

## 9. Synthetic Data Policy
- Strictly dummy/synthetic data used for user accounts, stock symbols, and orders (RULE-04). Zero Virtusa confidential or customer-sensitive data.

---

## 10. Security Expectations
- Passwords hashed using strong bcrypt KDF (`passlib`) before storage (NFR-03).
- Plaintext credentials and secrets strictly excluded from logs and git history.
- Authorization enforced at controller middleware layer via JWT claims (NFR-04).

---

## 11. Out-of-Scope Functionality
- Real exchange connectivity and real order-matching engine.
- Real clearinghouse or settlement infrastructure (T+1).
- WebSocket streaming market data.
- Margin, leverage, options, derivatives, or multi-currency FX trading.
- Real KYC document processing workflow (stubbed flag used).
