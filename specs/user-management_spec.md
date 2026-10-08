# User & Role Management Specification
**Feature:** User Onboarding, Authentication, & Administrative Role Partitioning  
**AC References:** AC-01, AC-02  

---

## 1. Purpose
Define requirements for customer registration, account state initialization, authentication token generation, administrative role management (`CUSTOMER`, `ADMIN`, `SUSPENDED`), and security audit trail logging.

---

## 2. Scope
- Customer self-serve registration.
- Account state initialization (`ACTIVE` state with `role = CUSTOMER`).
- Admin-initiated role updates.
- Audit logging of role update actions with actor ID and server timestamp.

---

## 3. Actors
- **Guest / Unauthenticated User:** Can register a new account.
- **Customer:** Authenticated user holding `CUSTOMER` role.
- **Admin:** Authenticated user holding `ADMIN` role.

---

## 4. User Journeys
1. **User Registration:** Guest posts email & password → System validates payload → Hashes password using bcrypt → Creates UserModel in `ACTIVE` state with `role = CUSTOMER` → Returns user DTO.
2. **Admin Role Update:** Admin posts target user ID & new role → System validates actor role = `ADMIN` → Updates target user role → Emits AuditLog entry with actor ID and timestamp → Returns updated user DTO.

---

## 5. Business Rules
- **Rule UM-01:** Duplicate email registrations MUST be rejected with HTTP 400 Bad Request.
- **Rule UM-02:** New customer accounts MUST be initialized in `ACTIVE` state with `role = CUSTOMER` (AC-01).
- **Rule UM-03:** Only users with `ADMIN` role can change account roles (AC-02). Non-admin attempts MUST raise `PermissionDeniedException` / HTTP 403 Forbidden.
- **Rule UM-04:** Every role update MUST generate an immutable entry in `audit_logs` capturing `actor_id`, `action`, `target_user_id`, and `timestamp` (AC-02).

---

## 6. Domain Model
```python
class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    SUSPENDED = "SUSPENDED"

class AccountState(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
```

---

## 7. API Requirements
### Endpoints
- `POST /api/v1/auth/register` — Register new customer account.
- `POST /api/v1/auth/login` — Authenticate and receive JWT token.
- `PUT /api/v1/admin/users/{user_id}/role` — Admin role update endpoint.

---

## 8. Error Handling
- Invalid email or weak password -> `422 Unprocessable Entity`.
- Existing email -> `400 Bad Request` ("Email already registered").
- Non-admin role update attempt -> `403 Forbidden` (`PermissionDeniedException`).
- Target user not found -> `404 Not Found` (`EntityNotFoundException`).

---

## 9. Security Requirements
- Passwords MUST be hashed via bcrypt before database insertion (NFR-03).
- Plaintext credentials MUST NEVER be written to stdout or JSON logs.
- Admin endpoints MUST enforce `ADMIN` role check in API middleware (NFR-04).

---

## 10. Acceptance Criteria

### AC-01: Customer Registration
```gherkin
Given a guest user with a valid email "trader@marketscope.com" and password "SecurePass123!"
When the user submits the registration request to "POST /api/v1/auth/register"
Then the account is created successfully
And the account state is initialized to "ACTIVE"
And the account role is assigned to "CUSTOMER"
And the password stored in the database is hashed using bcrypt
```

### AC-02: Admin Role Management & Auditing
```gherkin
Given an authenticated user with "ADMIN" role (actor ID = 1)
And an existing user account with ID = 2 and role = "CUSTOMER"
When the admin submits a role update request for user 2 setting target_role = "SUSPENDED"
Then the target user's role is updated to "SUSPENDED"
And an audit log record is created with actor_id = 1, target_user_id = 2, action = "UPDATE_USER_ROLE", and a server-side timestamp
```

---

## 11. Negative Test Cases
- **NT-UM-01:** Submit registration with an already existing email -> Expect HTTP 400.
- **NT-UM-02:** User with `CUSTOMER` role attempts to update another user's role -> Expect HTTP 403 `PermissionDeniedException`.
- **NT-UM-03:** Admin attempts role update for non-existent user ID 9999 -> Expect HTTP 404.

---

## 12. Non-Functional Requirements
- **NFR-03:** Passwords stored using bcrypt; zero plaintext credential logging.
- **NFR-04:** Authentication & role partitioning at controller middleware layer.

---

## 13. Dependencies
- Depends on `src/core/security.py` passlib module.
- Depends on `src/domain/role_policy.py` validation logic.
