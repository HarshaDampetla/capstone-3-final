# Substrate Agents Directory & Table of Contents

This repository defines specialized AI agents under `.claude/agents/` to execute autonomous, spec-driven development sprint tasks for MarketScope.

| Agent Name | Role & Responsibility | Definition File |
|---|---|---|
| **`order-lifecycle-agent`** | Implements and validates order state transitions, funds checks, and execution immutability. | `.claude/agents/order-lifecycle-agent.md` |
| **`portfolio-stats-agent`** | Computes and validates portfolio metrics, holdings value, and P&L analytics using Python `Decimal`. | `.claude/agents/portfolio-stats-agent.md` |
| **`security-reviewer-agent`** | Audits authentication, role partitioning, password hashing, and credentials security. | `.claude/agents/security-reviewer-agent.md` |
| **`architecture-test-agent`** | Writes structural architecture tests and verifies layer isolation contracts (`import-linter`). | `.claude/agents/architecture-test-agent.md` |
| **`user-management-agent`** | Manages user registration, role updates (`CUSTOMER`/`ADMIN`/`SUSPENDED`), and security auditing. | `.claude/agents/user-management-agent.md` |
| **`crud-scaffolder-agent`** | Technical agent for generating layered FastAPI CRUD endpoints, services, and repositories. | `.claude/agents/crud-scaffolder-agent.md` |
| **`watchlist-validator-agent`** | Validates watchlist count limits (max 10) and atomic operation invariants. | `.claude/agents/watchlist-validator-agent.md` |
| **`ac-test-generator-agent`** | Scaffolds AC-tagged pytest test files referencing `AC-NN` identifiers. | `.claude/agents/ac-test-generator-agent.md` |
| **`financial-rules-agent`** | Enforces zero floating-point math across domain models and P&L policy files. | `.claude/agents/financial-rules-agent.md` |
| **`documentation-agent`** | Generates business case docs, architecture diagrams, and TDD evidence. | `.claude/agents/documentation-agent.md` |
