# MarketScope — Root Workspace Guidelines & Governance Rules

## Project Identity
- **Title:** MarketScope — Stock Trading & Portfolio Analytics Platform
- **Business Case ID:** BC-AINE-006
- **Domain:** FinTech — Capital Markets / Brokerage

---

## Mandated AI-Native Governance Invariants

1. **No-Hand-Coding Rule:**
   All production code, unit tests, database schema migrations, and frontend components MUST be generated exclusively by Claude Code agents under human supervision. Hand edits are restricted to specifications, `CLAUDE.md` hierarchy, agent prompts, skills, commands, and hooks.

2. **Spec-Is-Truth Rule:**
   Specifications in `specs/` are authoritative. Whenever code and specification conflict, the specification wins. Update the spec deliberately, then regenerate code.

3. **PR-Only Merge Rule:**
   Zero direct commits to `main`. All changes must flow through agent-reviewed feature branches via non-fast-forward pull requests (`git merge --no-ff`).

4. **Strict Fixed-Point Financial Precision (NFR-01):**
   Prices, quantities, available cash, and P&L calculations MUST use Python `Decimal` exclusively. Floating-point numbers (`float`) are strictly forbidden for financial calculations.

5. **Layered Architectural Boundary (ARCH-01, NFR-04, NFR-08):**
   - API Controllers (`src/api/` or `backend/app/api/`) -> Service Layer -> Repositories -> Database.
   - API Controllers MUST NOT access ORM Repositories directly.
   - Domain layer (`src/domain/` or `backend/app/domain/`) MUST remain isolated with zero external imports.
   - Business logic belongs strictly inside Domain Policies or Service Layer. Controllers must remain thin wrappers.

6. **Authentication & Role Authorization Mandatory (NFR-04):**
   Authentication is enforced at the controller middleware layer. Endpoints must be strictly partitioned between `ADMIN` and `CUSTOMER` roles.

7. **Executed Order Immutability (NFR-02):**
   Trade records and executed orders (`EXECUTED` status) post-execution are append-only and immutable — no post-execution edits or deletes.

8. **Stock Catalog Soft-Delete (AC-03):**
   Stock deletion moves a symbol to `DELETED` / `DELISTED` status. Symbols are never hard-deleted from the database.

9. **Acceptance Criteria & Test Tagging (TECH-04, TECH-05):**
   All feature Acceptance Criteria must have at least one corresponding test tagged with its identifier (`@pytest.mark.ac("AC-NN")`).

10. **Synthetic-Data & Security Rule (NFR-03):**
    Use strictly dummy/synthetic data. Passwords must be hashed using bcrypt/argon2. Plaintext credentials and secrets must NEVER be logged or committed.

---

## Directory Hierarchy & Guidelines

- `/specs/CLAUDE.md` — Specification & AC-NN formatting rules
- `/backend/CLAUDE.md` — Backend Python & FastAPI conventions
- `/backend/app/CLAUDE.md` — Layered backend application guidelines
- `/backend/app/domain/CLAUDE.md` — Domain isolation & Decimal math rules
- `/backend/tests/CLAUDE.md` — Architecture & unit test tagging rules
- `/frontend/CLAUDE.md` — React, TypeScript & Vite UI conventions
- `AGENTS.md` — Table of contents for substrate agents in `.claude/agents/`
