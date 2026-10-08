# Backend Application Module (`backend/app/` or `src/`) Guidelines

## Layer Boundaries & Separation of Concerns

1. **Controllers / API (`api/`):**
   - Handles HTTP routing, input validation (Pydantic), and response status codes.
   - Must be thin. Must NOT contain domain logic or direct DB repository queries.
   - Controllers invoke Application Services.

2. **Services (`services/`):**
   - Application orchestration layer.
   - Orchestrates domain policy validations and repository persistence transactions.

3. **Repositories (`repositories/`):**
   - Encapsulates database queries using SQLAlchemy ORM.
   - Abstracts persistence from the rest of the application.

4. **Domain (`domain/`):**
   - Core domain logic and business rules. Completely isolated from web and persistence frameworks.
