# Watchlist Validator Agent Definition

## Purpose
The `watchlist-validator-agent` validates customer watchlist creation (name + >= 1 symbol, max 10 watchlists per user) and atomic update operations (`WatchlistUpdateException`).

## Responsibilities
1. Validate watchlist creation limits per customer (max 10 watchlists, AC-04).
2. Validate atomic symbol operations and raise `WatchlistUpdateException` on partial or invalid updates (AC-05).

## Inputs
- `specs/watchlist_spec.md`.
- Watchlist creation payloads.

## Outputs
- `src/domain/watchlist_policy.py` policy methods.
- `tests/unit/test_watchlist_policy.py` with `@pytest.mark.ac("AC-04")` and `@pytest.mark.ac("AC-05")` tags.

## Constraints
- Atomic symbol updates MUST either complete entirely or throw `WatchlistUpdateException`.

## Validation
- Run `pytest tests/unit/test_watchlist_policy.py`.

## Failure Handling
- If watchlist count is >= 10, abort immediately with `WatchlistUpdateException`.
