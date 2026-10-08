# Backend Guidelines & Standards

## Architecture & Code Rules
- All backend code is written in Python 3.11+ using FastAPI, SQLAlchemy 2.0, Pydantic v2, and Alembic.
- **Financial Rule:** All monetary fields (prices, holdings, cash, P&L) MUST use Python `Decimal`. NEVER use floating-point numbers.
- **Layering Rule:** API Controllers -> Services -> Repositories -> Database. Controllers CANNOT access Repositories directly.
- **Security Rule:** Password hashing must use bcrypt (`passlib`). Passwords and secrets must NEVER be logged in plaintext.
- **Immutability Rule:** Executed orders and trade records are append-only.
- **Catalog Rule:** Stock deletions are soft-deletes (`DELETED` status).
- **Test Rule:** All endpoints and policies require tests tagged with `@pytest.mark.ac("AC-NN")`.
