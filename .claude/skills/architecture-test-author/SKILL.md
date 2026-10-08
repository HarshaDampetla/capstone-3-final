---
name: architecture-test-author
description: Authoring structural architecture tests checking layer isolation and dependency rules.
---

# Architecture Test Author Skill

## Purpose & Usage
Use this skill when writing architecture tests under `tests/architecture/` or configuring `.importlinter` rules (ARCH-01, ARCH-02).

## Layering Rules to Enforce

1. Controllers (`src/api/`) -> Services (`src/services/`) -> Repositories (`src/repositories/`) -> Domain (`src/domain/`).
2. Controllers MUST NOT import repositories directly.
3. Domain MUST have 0 dependencies on API, Services, Repositories, or DB ORM.

## Verification Commands
```bash
pytest tests/architecture/ -v
lint-imports
```
