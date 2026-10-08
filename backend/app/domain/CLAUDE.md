# Domain Layer (`domain/`) Invariants

## Domain Invariants

1. **Zero External Framework Imports:**
   Domain modules MUST NOT import FastAPI, SQLAlchemy, or HTTP libraries.
2. **Fixed-Point Financial Math (NFR-01):**
   All financial arithmetic (P&L, total invested, order quote prices, available cash) MUST use Python `Decimal`. Floating-point numbers are prohibited.
3. **Pure Business Policies:**
   Role updates, watchlist limits (max 10), atomic updates, order state transitions (`PENDING` -> `EXECUTED`/`CANCELLED`/`REJECTED`), and funds validation MUST be executed via domain policy classes.
