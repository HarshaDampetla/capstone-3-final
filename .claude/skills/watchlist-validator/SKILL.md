---
name: watchlist-validator
description: Enforces maximum 10 watchlists per customer and atomic symbol updates.
---

# Watchlist Validator Skill

## Purpose & Usage
Use this skill when developing or auditing customer watchlist operations (AC-04, AC-05).

## Business Rules

1. **Watchlist Limit (AC-04):**
   - Check current customer watchlist count before creation.
   - If `count >= 10`, raise `WatchlistUpdateException("Customer cannot hold more than 10 watchlists.")`.

2. **Atomic Operations (AC-05):**
   - Watchlist creation requires a valid non-empty name and at least 1 symbol.
   - Rename, add/remove symbols, and delete operations MUST execute atomically within a database transaction. Partial updates MUST be rolled back and throw `WatchlistUpdateException`.

## Verification Command
```bash
pytest tests/unit/test_watchlist_policy.py -v
```
