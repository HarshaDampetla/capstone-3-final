# Test Suite (`tests/`) Guidelines

## Test Organization

- `tests/architecture/` — Structural tests checking layer isolation via `import-linter` & `pytest`.
- `tests/unit/` — Fast unit tests for domain policies, math, and services.
- `tests/integration/` — API endpoint tests using `httpx.AsyncClient` or `TestClient`.
- `tests/ui/` — Playwright browser tests and visual snapshot files in `snapshots/`.

## Standards

- All tests for specific Acceptance Criteria MUST be tagged with `@pytest.mark.ac("AC-NN")`.
- Assert financial calculations with exact `Decimal` equality.
