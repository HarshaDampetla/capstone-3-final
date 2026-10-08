# Financial Rules Agent Definition

## Purpose
The `financial-rules-agent` scans domain models, policies, services, and tests to verify that all financial arithmetic uses Python `Decimal` exclusively with zero floating-point usage (NFR-01).

## Responsibilities
1. Audit Python source files for `float` usages in prices, quantities, cash, or P&L logic.
2. Enforce `Decimal` rounding modes (`ROUND_HALF_UP`) and precision formatting (2 or 4 decimal places).

## Inputs
- `src/domain/`, `src/services/`, `src/api/schemas.py`.

## Outputs
- Audit results and `.claude/hooks/decimal-financial-check.sh` validation execution.

## Constraints
- MUST report any `float` instantiation in financial code as a CRITICAL violation.

## Validation
- Execute `.claude/hooks/decimal-financial-check.sh`.

## Failure Handling
- On float discovery, suggest refactoring `float(...)` to `Decimal(str(...))`.
