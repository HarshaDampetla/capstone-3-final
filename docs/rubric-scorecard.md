# MarketScope — Rubric Scorecard & Evaluation Mapping
**Business Case ID:** BC-AINE-006  
**Total Marks:** 100 Marks  
**Evaluation Mode:** Automated review against AI-Native Engineering Rubric (21 Parameters across 5 Categories)  

---

## Grade Bands Reference

| Grade Band | Score Range | Objective Target for MarketScope |
|---|---|---|
| **Distinction** | **≥ 90 Marks** | **Target Grade** (Complete Substrate + All Mandatory & Good-to-Have Deliverables) |
| **Merit** | 75 – 89 Marks | Fallback |
| **Pass** | 60 – 74 Marks | Minimum acceptable |
| **Not Yet Passed** | < 60 Marks | Unacceptable / Failure |

---

## Rubric Breakdown by Category (100 Marks Total)

### Category 1: Claude Code Specs / AI-Native Substrate (40 Marks)

| Parameter ID | Parameter Description | Allocation | Required Artifact / Evidence | Target Strategy & Self-Audit |
|---|---|---|---|---|
| **SUB-01** | Root spec & feature specs with explicit Acceptance Criteria | 5 Marks | `specs/app_spec.md`, `specs/user-management_spec.md`, `specs/stock-catalog_spec.md`, `specs/watchlist_spec.md`, `specs/order_spec.md`, `specs/portfolio_spec.md`, `specs/analytics_spec.md` | Each spec must contain explicit Given-When-Then / AC-NN sections. |
| **SUB-02** | Layered `CLAUDE.md` hierarchy & `AGENTS.md` | 5 Marks | `CLAUDE.md`, `src/CLAUDE.md`, `tests/CLAUDE.md`, `specs/CLAUDE.md`, `AGENTS.md` | Root + per-module + per-folder rules; `AGENTS.md` acts strictly as table of contents. |
| **SUB-03** | Project-specific skills under `.claude/skills/` | 5 Marks | `.claude/skills/crud-controller-scaffolder/SKILL.md`, `.claude/skills/stats-aggregator/SKILL.md`, `.claude/skills/watchlist-validator/SKILL.md`, `.claude/skills/portfolio-pnl-calculator/SKILL.md` | At least 2 custom skills created and documented. |
| **SUB-04** | Project-specific custom commands under `.claude/commands/` | 4 Marks | `.claude/commands/run-arch-tests.sh`, `.claude/commands/check-immutability.sh`, `.claude/commands/generate-pnl-report.sh` | Custom commands beyond Harness defaults. |
| **SUB-05** | Project-specific hooks under `.claude/hooks/` | 4 Marks | `.claude/hooks/password-hash-check.sh`, `.claude/hooks/role-boundary-check.sh`, `.claude/hooks/executed-order-immutability-check.sh` | Executable bash scripts enforcing safety invariants before commit/tool execution. |
| **SUB-06** | Project-specific agents under `.claude/agents/` | 5 Marks | `.claude/agents/portfolio-stats-agent.md`, `.claude/agents/order-lifecycle-agent.md`, `.claude/agents/user-management-agent.md` | Custom agents in `.claude/agents/` with clear roles and prompts. |
| **SUB-07** | Programmatic Claude Agent SDK usage in `scripts/` | 4 Marks | `scripts/agent_evaluator.py` | Python script importing and invoking agent workflows programmatically. |
| **SUB-08** | Custom `plugin.json` packaging substrate | 4 Marks | `.claude/plugin.json` / `plugin.json` | Valid plugin manifest bundling tools, agents, skills, and commands. |
| **SUB-09** | Debugging log / Post-mortem document in `docs/` | 2 Marks | `docs/post-mortem-01.md`, `docs/debugging-log.md` | Evidencing environment-first resolution of an issue. |
| **SUB-10** | Playwright MCP in `.mcp.json` & Evaluator integration | 2 Marks | `.mcp.json`, `tests/ui/` | Active Playwright MCP configuration used by evaluator for UI testing. |
| **SUB TOTAL** | **Claude Code Specs / Substrate** | **40 Marks** | | **Full 40/40 Target** |

---

### Category 2: Business Understanding (20 Marks)

| Parameter ID | Parameter Description | Allocation | Required Artifact / Evidence | Target Strategy & Self-Audit |
|---|---|---|---|---|
| **BUS-01** | `docs/business-case.md` completeness | 6 Marks | `docs/business-case.md` | Problem, target users, success metrics, domain rules, and value proposition fully detailed. |
| **BUS-02** | Domain rule / policy / validator implementation | 6 Marks | `src/domain/watchlist_policy.py`, `src/domain/order_policy.py`, `src/domain/pnl_calculator.py`, `src/domain/role_validator.py` | At least 4 distinct policy/validator modules under `src/domain/`. |
| **BUS-03** | Frontend responsive UI evidence | 4 Marks | `frontend/` (React/Vue/HTML) + Playwright UI snapshots | Working UI with responsive layout verified via snapshots. |
| **BUS-04** | Acceptance criteria in testable format | 4 Marks | Specs & test files | Given-When-Then or AC-NN identifiers in at least 4 feature specs. |
| **SUB TOTAL** | **Business Understanding** | **20 Marks** | | **Full 20/20 Target** |

---

### Category 3: Architectural Discipline (8 Marks)

| Parameter ID | Parameter Description | Allocation | Required Artifact / Evidence | Target Strategy & Self-Audit |
|---|---|---|---|---|
| **ARC-01** | Architecture test suite (>= 3 structural tests) | 3 Marks | `tests/architecture/test_layering.py`, `test_dependencies.py`, `test_domain_isolation.py` | At least 3 automated tests checking layer isolation & boundaries. |
| **ARC-02** | ArchUnit / `import-linter` layering enforcement | 2 Marks | `.importlinter` or ArchUnit config | Configured tool blocking illegal cross-layer imports (e.g. Domain -> Controller). |
| **ARC-03** | TDD discipline doc (`docs/tdd.md`) & test history | 3 Marks | `docs/tdd.md` & >= 10 test commits | Documented Red-Green-Refactor flow with AC-08 worked example & commit evidence. |
| **SUB TOTAL** | **Architectural Discipline** | **8 Marks** | | **Full 8/8 Target** |

---

### Category 4: Technical Implementation (26 Marks)

| Parameter ID | Parameter Description | Allocation | Required Artifact / Evidence | Target Strategy & Self-Audit |
|---|---|---|---|---|
| **TEC-01** | Architecture document (`docs/architecture.md`) with Mermaid diagram | 6 Marks | `docs/architecture.md` | Mermaid sequence & layer diagrams explaining request flow & modules. |
| **TEC-02** | Substantive codebase size (>= 3000 LOC generated) | 6 Marks | `src/`, `tests/`, `migrations/` | > 3000 lines of meaningful, modular, agent-generated Python/JS/SQL code. |
| **TEC-03** | Playwright UI validation & snapshot directory | 5 Marks | `tests/ui/`, `snapshots/` | Automated UI test scripts generating and comparing visual snapshots. |
| **TEC-04** | Test tagging with AC IDs | 5 Marks | `tests/` with `@pytest.mark.ac("AC-01")` or `# AC-01` tags | 100% coverage of AC-01 through AC-10 with explicit AC tags in tests. |
| **TEC-05** | Unit tests (>= 20) & coverage report artifact | 4 Marks | `tests/unit/`, `coverage.xml` | At least 20 unit tests generating `coverage.xml` / `lcov.info` with tool in dependencies. |
| **SUB TOTAL** | **Technical Implementation** | **26 Marks** | | **Full 26/26 Target** |

---

### Category 5: CI/CD (6 Marks)

| Parameter ID | Parameter Description | Allocation | Required Artifact / Evidence | Target Strategy & Self-Audit |
|---|---|---|---|---|
| **CIC-01** | CI pipeline configuration with build & test pipeline | 2 Marks | `.github/workflows/ci.yml` or `.gitlab-ci.yml` | Automated build, lint, arch-test, unit-test, and coverage step. |
| **CIC-02** | Claude Code Action / agentic quality gate in CI | 2 Marks | `.github/workflows/ci.yml` step | Automated spec/rule validator action step in CI workflow. |
| **CIC-03** | At least 3 PR-driven merges (`git merge --no-ff`) & 0 direct commits to `main` | 2 Marks | Git commit history | Clean PR graph with non-fast-forward merge commits. |
| **SUB TOTAL** | **CI/CD** | **6 Marks** | | **Full 6/6 Target** |

---

## Scoring Summary & Target Distinction Blueprint

| Category | Max Marks | Targeted Score | Key Success Factors |
|---|---|---|---|
| 1. Claude Code Specs / AI-Native Substrate | 40 | 40 | Specs, CLAUDE.md hierarchy, skills, commands, hooks, agents, SDK script, plugin.json, post-mortem, Playwright MCP |
| 2. Business Understanding | 20 | 20 | `business-case.md`, 4 domain policies, web UI, testable AC-NN format |
| 3. Architectural Discipline | 8 | 8 | 3 structural arch tests, import-linter config, `docs/tdd.md` with commit trail |
| 4. Technical Implementation | 26 | 26 | `architecture.md` diagram, >3000 LOC agent code, UI snapshots, AC-tagged tests, >=20 unit tests + `coverage.xml` |
| 5. CI/CD | 6 | 6 | CI workflow script, Claude Code Action step, >= 3 PR `--no-ff` merges |
| **TOTAL** | **100** | **100** | **Distinction Grade Band Target (≥ 90 Marks)** |
