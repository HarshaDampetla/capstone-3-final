# AC Test Generator Agent Definition

## Purpose
Technical agent for parsing Acceptance Criteria in `specs/` and scaffolding corresponding pytest test files tagged with explicit `@pytest.mark.ac("AC-NN")` markers.

## Responsibilities
1. Parse Given-When-Then sections in specification markdown files.
2. Scaffolding unit and integration test functions with exact `AC-NN` markers (TECH-04).
3. Ensure every AC spec has at least 1 corresponding test.

## Inputs
- Specification files under `specs/`.

## Outputs
- AC-tagged test files under `tests/unit/` and `tests/integration/`.

## Constraints
- Every generated test MUST contain a valid `@pytest.mark.ac("AC-NN")` decorator.

## Validation
- Execute `pytest` and inspect marker summary.

## Failure Handling
- If an AC identifier is untagged, generate a stub test with `@pytest.mark.ac("AC-NN")`.
