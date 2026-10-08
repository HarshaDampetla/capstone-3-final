# User Management Agent Definition

## Purpose
The `user-management-agent` manages customer registration, initial `ACTIVE` state assignment, `CUSTOMER` role assignment, administrative role updates (`CUSTOMER`/`ADMIN`/`SUSPENDED`), and audit logging.

## Responsibilities
1. Implement customer registration endpoint with default `ACTIVE` state and `CUSTOMER` role (AC-01).
2. Implement admin role update endpoint with actor ID and timestamp auditing (AC-02).
3. Validate user management inputs using Pydantic DTOs and bcrypt password hashing.

## Inputs
- `specs/user-management_spec.md`.
- User registration payloads and role update requests.

## Outputs
- `src/repositories/user_repository.py` methods.
- `src/domain/role_policy.py` validation logic.
- `tests/unit/test_auth.py` with `@pytest.mark.ac("AC-01")` and `@pytest.mark.ac("AC-02")` tags.

## Constraints
- Password plaintext MUST be hashed via bcrypt immediately upon receipt (NFR-03).
- Role updates MUST record an entry in `audit_logs` table (AC-02).

## Validation
- Execute `pytest tests/unit/test_auth.py`.

## Failure Handling
- If duplicate email is submitted, raise HTTP 400 with a clear domain error message.
