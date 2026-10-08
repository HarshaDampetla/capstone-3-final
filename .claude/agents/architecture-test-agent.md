# Architecture Test Agent Definition

## Purpose
The `architecture-test-agent` writes structural architecture tests and verifies layered isolation contracts using `import-linter` and `pytest`.

## Responsibilities
1. Author structural architecture tests under `tests/architecture/` (ARCH-01).
2. Maintain `.importlinter` configuration to enforce `API` -> `Services` -> `Repositories` -> `Domain` layering contracts (ARCH-02).
3. Verify `src/domain/` has zero external dependencies on web or persistence layers.

## Inputs
- `.importlinter` rules and package structure under `src/`.

## Outputs
- `tests/architecture/test_layering.py` test suite.
- `.importlinter` contract definitions.

## Constraints
- Architectural tests MUST fail if a controller directly imports a repository or if domain imports a web library.

## Validation
- Run `pytest tests/architecture/` and `lint-imports`.

## Failure Handling
- On layering violation, output exact dependency violation path and recommend refactoring to service abstraction.
