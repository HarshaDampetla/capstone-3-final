# Source Code (`src/`) Architecture Guidelines

## Layering Rules

1. **`src/domain/`**:
   - Contains core business rules, entity domain models, custom exceptions, and financial calculation logic.
   - **MUST NOT** import anything from `src.api`, `src.services`, `src.repositories`, or `src.db`.
   - All numbers representing currency or trade quantities MUST be `Decimal`.

2. **`src/repositories/`**:
   - Contains data access interfaces and SQLAlchemy database implementations.
   - Handles SQL queries, transactions, and entity mapping.

3. **`src/services/`**:
   - Application orchestration layer.
   - Invokes domain policy checks and delegates persistence to repositories.

4. **`src/api/`**:
   - FastAPI routers, request schemas, response models, and authentication middleware.
   - Controllers MUST be thin wrappers delegating to services. No domain logic in routers.
