# MarketScope — Stock Trading & Portfolio Analytics Platform
## Complete Capstone Requirements & Traceability Matrix
**Business Case ID:** BC-AINE-006  
**Domain:** FinTech — Capital Markets / Brokerage  
**Project Type:** AI-Native Engineering Capstone  

---

### 1. Functional Acceptance Criteria (AC)

| Requirement ID | Requirement | Category | Marks | Required Artifact | Implementation Location | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| **AC-01** | Customer can register with email & password; account created in `ACTIVE` state with `role = CUSTOMER` | Functional | Part of Tech Impl (26m) | `specs/user-management_spec.md` | `src/auth/` or `src/users/` | `tests/unit/test_auth.py` / AC-01 tag | PLANNED |
| **AC-02** | Admin can update a user's role (`CUSTOMER`, `ADMIN`, `SUSPENDED`); action audited with actor & timestamp | Functional | Part of Tech Impl (26m) | `specs/user-management_spec.md` | `src/users/` | `tests/unit/test_user_admin.py` / AC-02 tag | PLANNED |
| **AC-03** | Stock catalog supports full CRUD for `ADMIN` role; soft-delete moves symbol to `DELETED` status (never hard-deleted) | Functional | Part of Tech Impl (26m) | `specs/stock-catalog_spec.md` | `src/catalog/` | `tests/unit/test_catalog.py` / AC-03 tag | PLANNED |
| **AC-04** | Customer can create watchlist with name & >= 1 symbol; max 10 watchlists per customer | Functional | Part of Tech Impl (26m) | `specs/watchlist_spec.md` | `src/watchlist/` | `tests/unit/test_watchlist.py` / AC-04 tag | PLANNED |
| **AC-05** | Watchlist operations (rename, add/remove symbols, delete) execute atomically; partial updates raise `WatchlistUpdateException` | Functional | Part of Tech Impl (26m) | `specs/watchlist_spec.md` | `src/watchlist/` | `tests/unit/test_watchlist.py` / AC-05 tag | PLANNED |
| **AC-06** | Customer can place market or limit order (`BUY` or `SELL`); order enters `PENDING` state with server-side timestamp | Functional | Part of Tech Impl (26m) | `specs/order_spec.md` | `src/order/` | `tests/unit/test_order.py` / AC-06 tag | PLANNED |
| **AC-07** | Order lifecycle `PENDING` → `EXECUTED` / `CANCELLED` / `REJECTED` enforced; invalid transitions raise `InvalidOrderStateException` | Functional | Part of Tech Impl (26m) | `specs/order_spec.md` | `src/order/` | `tests/unit/test_order_lifecycle.py` / AC-07 tag | PLANNED |
| **AC-08** | `BUY` order fails with `InsufficientFundsException` when `quote_price × quantity > available_cash` | Functional | Part of Tech Impl (26m) | `specs/order_spec.md` | `src/order/` & `src/domain/` | `tests/unit/test_order_funds.py` / AC-08 tag | PLANNED |
| **AC-09** | Portfolio statistics endpoint returns `total_invested`, `current_value`, `absolute_pnl`, and `percent_pnl` for requesting customer | Functional | Part of Tech Impl (26m) | `specs/portfolio_spec.md` | `src/portfolio/` & `src/domain/` | `tests/unit/test_portfolio_stats.py` / AC-09 tag | PLANNED |
| **AC-10** | Daily statistics endpoint returns top 5 gainers and top 5 losers from requesting customer's current holdings | Functional | Part of Tech Impl (26m) | `specs/analytics_spec.md` | `src/analytics/` & `src/domain/` | `tests/unit/test_analytics.py` / AC-10 tag | PLANNED |

---

### 2. Non-Functional Requirements (NFR)

| Requirement ID | Requirement | Category | Marks | Required Artifact | Implementation Location | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| **NFR-01** | Price, quantity, and P&L values computed in fixed-point (`Decimal` / `BigDecimal`) — never floating-point | Non-Functional | Part of Tech Impl (26m) | Domain models & rules | `src/domain/` | Unit tests verifying Decimal precision / Hook blocking float P&L | PLANNED |
| **NFR-02** | Trade records and executed orders are append-only — no edits or deletes post-execution | Non-Functional | Part of Tech Impl (26m) | Immutability guardrails | `src/order/` & `src/domain/` | Automated immutability test / hook check | PLANNED |
| **NFR-03** | Passwords stored using strong KDF (`bcrypt` / `argon2`); plaintext credentials never logged | Non-Functional | Part of Tech Impl (26m) | Security config & hooks | `src/auth/` | `tests/security/test_password_hashing.py` & `.claude/hooks/password-hash-check.sh` | PLANNED |
| **NFR-04** | Authentication enforced at controller layer; `ADMIN` and `CUSTOMER` endpoints partitioned by role | Non-Functional | Part of Tech Impl (26m) | Middleware / Guards | `src/api/middleware.py` | Role-boundary security tests | PLANNED |
| **NFR-05** | Database migrations are append-only | Non-Functional | Part of Tech Impl (26m) | Migration scripts | `migrations/` or `alembic/` | Migration verification test | PLANNED |
| **NFR-06** | Structured JSON logs with request correlation IDs | Non-Functional | Part of Tech Impl (26m) | Logging module | `src/common/logging.py` | Log format integration tests | PLANNED |
| **NFR-07** | Health endpoint returns 200 within 1 second of a successful startup | Non-Functional | Part of Tech Impl (26m) | Health router | `src/api/health.py` | Integration test / curl latency check | PLANNED |
| **NFR-08** | Architecture rules enforced as automated tests (e.g., ADMIN endpoints unreachable by CUSTOMER role; executed orders immutable) | Non-Functional | Architectural Discipline (8m) | Architecture test suite | `tests/architecture/` | `pytest` architecture suite / `import-linter` | PLANNED |

---

### 3. AI-Native Engineering Substrate Requirements (AINE)

| Requirement ID | Requirement | Category | Marks | Required Artifact | Implementation Location | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| **AINE-01** | Root spec (`specs/app_spec.md`) and per-feature specs (`specs/<feature>_spec.md`) with explicit Acceptance Criteria | AI-Native Substrate | 40 marks (Substrate) | Spec markdown files | `specs/` | Validated by spec-to-test traceability & Harness Evaluator | PLANNED |
| **AINE-02** | Layered `CLAUDE.md` hierarchy (root + per-module + per-folder) with `AGENTS.md` as TOC | AI-Native Substrate | 40 marks (Substrate) | `CLAUDE.md` files & `AGENTS.md` | `CLAUDE.md`, `src/CLAUDE.md`, `tests/CLAUDE.md`, `AGENTS.md` | Repository structure check | PLANNED |
| **AINE-03** | At least 2 project-specific skills under `.claude/skills/` (e.g., `crud-controller-scaffolder`, `stats-aggregator`, `portfolio-pnl-calculator`) | AI-Native Substrate | 40 marks (Substrate) | Skill definitions | `.claude/skills/` | Skill execution logs | PLANNED |
| **AINE-04** | At least 2 project-specific custom commands under `.claude/commands/` | AI-Native Substrate | 40 marks (Substrate) | Custom commands | `.claude/commands/` | Command execution logs | PLANNED |
| **AINE-05** | At least 2 project-specific hooks under `.claude/hooks/` (e.g., `password-hash-check.sh`, `role-boundary-check.sh`, `executed-order-immutability-check.sh`) | AI-Native Substrate | 40 marks (Substrate) | Shell hook scripts | `.claude/hooks/` | Pre-commit/tool execution hooks | PLANNED |
| **AINE-06** | At least 2 project-specific agents under `.claude/agents/` (domain or technical agents) | AI-Native Substrate | 40 marks (Substrate) | Agent prompt definitions | `.claude/agents/` | Agent activity logs | PLANNED |
| **AINE-07** | At least 1 programmatic Claude Agent SDK usage in `scripts/` | AI-Native Substrate | 40 marks (Substrate) | Python script using Anthropic/Claude Agent SDK | `scripts/agent_evaluator.py` | Script execution output/log | PLANNED |
| **AINE-08** | Project `plugin.json` packaging substrate (in addition to Harness `plugin.json`) | AI-Native Substrate | 40 marks (Substrate) | Plugin manifest | `.claude/plugin.json` / `plugin.json` | Plugin validation check | PLANNED |
| **AINE-09** | At least 1 project-specific debugging log or post-mortem document under `docs/` | AI-Native Substrate | 40 marks (Substrate) | Debugging log / post-mortem | `docs/post-mortem-01.md` | Document review | PLANNED |
| **AINE-10** | Playwright MCP configured in `.mcp.json` and actively used by evaluator | AI-Native Substrate | 40 marks (Substrate) | `.mcp.json` | `.mcp.json` | Playwright UI test runs & snapshot directory | PLANNED |

---

### 4. Business Understanding & Domain Requirements (BUS)

| Requirement ID | Requirement | Category | Marks | Required Artifact | Implementation Location | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| **BUS-01** | `docs/business-case.md` covering problem, target users, success metrics, domain rules, and value proposition | Business Understanding | 20 marks | Business Case Doc | `docs/business-case.md` | Read by Reviewer Plugin | PLANNED |
| **BUS-02** | At least 4 rule / policy / validator files under `src/domain/` implementing trading & portfolio business rules | Business Understanding | 20 marks | Domain Policy Modules | `src/domain/` | Unit tests targeting policies | PLANNED |
| **BUS-03** | Frontend evidence (React / Angular / Vue) with at least 1 responsive layout | Business Understanding | 20 marks | Web UI app | `frontend/` or `src/web/` | Playwright UI snapshots | PLANNED |
| **BUS-04** | Acceptance criteria expressed in testable Given-When-Then or AC-NN format for at least 4 specs | Business Understanding | 20 marks | Feature Specs | `specs/*.md` | Traceability matrix check | PLANNED |

---

### 5. Architectural Discipline Requirements (ARCH)

| Requirement ID | Requirement | Category | Marks | Required Artifact | Implementation Location | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| **ARCH-01** | Architecture-test directory with at least 3 structural tests | Architectural Discipline | 8 marks | Arch tests | `tests/architecture/` | `pytest` test output | PLANNED |
| **ARCH-02** | Layering enforcement tool (`import-linter` or equivalent) configured | Architectural Discipline | 8 marks | Config file (`.importlinter` or equivalent) | Root / `tests/architecture/` | Architectural lint command run | PLANNED |
| **ARCH-03** | TDD discipline document (`docs/tdd.md`) & >= 10 test files committed demonstrating Red-Green-Refactor pattern | Architectural Discipline | 8 marks | TDD Document & Git history | `docs/tdd.md` & Git commit log | Git commit logs showing test-first commits | PLANNED |

---

### 6. Technical Implementation Requirements (TECH)

| Requirement ID | Requirement | Category | Marks | Required Artifact | Implementation Location | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| **TECH-01** | `docs/architecture.md` with >= 1 architecture diagram (Mermaid/image) & explicit layered structure | Technical Implementation | 26 marks | Architecture Doc | `docs/architecture.md` | Architecture review | PLANNED |
| **TECH-02** | Substantive codebase with >= 3000 lines of meaningful agent-generated code | Technical Implementation | 26 marks | Source code | `src/` & `tests/` | `cloc` / line count check | PLANNED |
| **TECH-03** | Playwright (or equivalent) UI validation with at least 1 snapshot directory | Technical Implementation | 26 marks | Playwright UI suite | `tests/ui/` & `snapshots/` | Snapshot images in repository | PLANNED |
| **TECH-04** | Tests tagged with AC IDs — every spec AC has at least 1 corresponding test | Technical Implementation | 26 marks | Test suite | `tests/` | AC-NN test run summary | PLANNED |
| **TECH-05** | At least 20 unit tests with coverage artifact (`coverage.xml` / `lcov.info`) & tool declared in dependencies | Technical Implementation | 26 marks | Coverage report & test suite | `tests/unit/` & `coverage.xml` | Coverage report file & dependencies | PLANNED |

---

### 7. CI/CD Requirements (CICD)

| Requirement ID | Requirement | Category | Marks | Required Artifact | Implementation Location | Test/Evidence | Status |
|---|---|---|---|---|---|---|---|
| **CICD-01** | CI pipeline config (`.gitlab-ci.yml` or `.github/workflows/ci.yml`) with build and test pipeline | CI/CD | 6 marks | CI configuration file | `.github/workflows/ci.yml` | Pipeline execution run | PLANNED |
| **CICD-02** | Claude Code Action (or equivalent agentic check) wired into CI workflow | CI/CD | 6 marks | CI workflow file | `.github/workflows/ci.yml` | Action step in workflow log | PLANNED |
| **CICD-03** | At least 3 PR-driven merges (`git merge --no-ff`); zero direct commits to main | CI/CD | 6 marks | Git repository history | Git commit log | `git log --graph --oneline` output | PLANNED |

---

### 8. Applicable Governance Rules (RULE)

| Requirement ID | Requirement | Category | Marks | Governance Impact | Enforced By | Violation Consequence | Status |
|---|---|---|---|---|---|---|---|
| **RULE-01** | **No-Hand-Coding Rule:** All production code, tests, and migrations generated by Claude Code agents. | Governance | Core Constraint | Zero manual coding allowed for code/tests/migrations. | Agent logs, PR history | Substrate disqualification | ACTIVE |
| **RULE-02** | **Spec-Is-Truth Rule:** Spec wins over code. Update spec first, then regenerate code. | Governance | Core Constraint | Keeps specs and code 100% aligned. | Harness Evaluator | Spec divergence penalty | ACTIVE |
| **RULE-03** | **PR-Only Merge Rule:** No direct commits to main; all code merged via agent-reviewed PRs. | Governance | Core Constraint | Ensures full PR traceability. | Git branch protection / CI rules | Direct commit penalty | ACTIVE |
| **RULE-04** | **Synthetic-Data Rule:** Use strictly synthetic/dummy data. | Governance | Compliance | Zero real customer or Virtusa sensitive data. | Seed script & reviewer check | Security/compliance breach | ACTIVE |

---

### 9. Deliverables Inventory (DELIV)

#### Mandatory Deliverables (10/10 Required)
1. **DELIV-M01:** Working Application (deployable locally via single command, seeded with dummy data, README quick-start)
2. **DELIV-M02:** `docs/business-case.md` (Problem, target users, metrics, domain rules, value prop)
3. **DELIV-M03:** Feature Specifications (`specs/app_spec.md` + per-feature specs with AC sections)
4. **DELIV-M04:** Layered `CLAUDE.md` Hierarchy (Root, module, folder levels + `AGENTS.md` TOC)
5. **DELIV-M05:** Project Agent Substrate (`.claude/agents/`, `.claude/skills/`, `.claude/commands/`, `.claude/hooks/`)
6. **DELIV-M06:** Claude Harness Engine Integration (Scaffolded, sprint contracts in `sprint-contracts/`, reviews in `specs/reviews/`)
7. **DELIV-M07:** Plugin & MCP Manifests (Project `plugin.json` and `.mcp.json` with Playwright MCP)
8. **DELIV-M08:** Automated Test Suite (Unit, Domain, P&L, Immutability, ArchUnit, AC-tagged, UI snapshot, Coverage XML)
9. **DELIV-M09:** CI/CD Pipeline (`.github/workflows/ci.yml` with Claude Code Action)
10. **DELIV-M10:** PR-Driven Git History (At least 3 `--no-ff` PR merges, zero direct pushes to `main`)

#### Good-to-Have Deliverables (5 Differentiation Artifacts)
11. **DELIV-G01:** Architecture & TDD Documentation (`docs/architecture.md` with C4/Sequence diagrams & `docs/tdd.md` with AC-08 worked example)
12. **DELIV-G02:** Autonomous Fix Loop Evidence (`docs/fix-loops/` recording agent auto-detection, reproduce, fix, PR)
13. **DELIV-G03:** Knowledge Deposit Log (`docs/knowledge-deposits.md` recording recurring mistake mitigations)
14. **DELIV-G04:** Multiple Sprint Cycles (Multi-sprint progression across feature domains)
15. **DELIV-G05:** Bonus Substrate Agents (`janitor-agent`, `performance-auditor-agent`, `doc-writer-agent`)
