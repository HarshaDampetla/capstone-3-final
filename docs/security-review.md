# MarketScope — Security Audit & Threat Review

**Business Case ID:** BC-AINE-006  
**System:** MarketScope Stock Trading Platform  
**Compliance Standard:** Role-Based Access Control (RBAC), OWASP Security Best Practices  

---

## 1. Authentication & Credentials Security

### Password Hashing
- **Algorithm:** Native `bcrypt` algorithm.
- **Safety Slicing:** Input passwords are sliced to a maximum of 72 bytes before hashing to prevent denial-of-service via oversized inputs.
- **Storage:** Plaintext passwords are NEVER logged or stored. Only salted bcrypt hash strings (`hashed_password`) are persisted in the database.

### JWT Bearer Authentication
- **Token Generation:** `create_access_token` in `src/core/security.py` signs JWT tokens using algorithm `HS256` and secret `SECRET_KEY`.
- **Claims:** JWT payload contains `sub` (User ID string) and `role` (User role).
- **Expiration:** Configurable token expiry (`ACCESS_TOKEN_EXPIRE_MINUTES`).

---

## 2. Authorization & Role Partitioning (NFR-04)

### Role Hierarchy & Matrix
```
User Roles:
├── CUSTOMER   (Standard trading, watchlists, portfolio analytics)
├── ADMIN      (User role management, stock catalog CRUD, order auditing)
└── SUSPENDED  (Access denied to all protected endpoints)
```

| Resource / Endpoint | `CUSTOMER` | `ADMIN` | `SUSPENDED` |
|---|---|---|---|
| `POST /api/v1/auth/register` | ✅ Public | ✅ Public | ✅ Public |
| `POST /api/v1/auth/login` | ✅ Public | ✅ Public | ❌ Account Suspended (403) |
| `GET /api/v1/catalog` | ✅ Allowed | ✅ Allowed | ❌ Denied (403) |
| `POST /api/v1/orders` | ✅ Allowed | ✅ Allowed | ❌ Denied (403) |
| `DELETE /api/v1/orders/{id}` | ✅ Own Orders | ✅ Own Orders | ❌ Denied (403) |
| `GET /api/v1/portfolio/stats` | ✅ Own Stats | ✅ Own Stats | ❌ Denied (403) |
| `POST /api/v1/admin/catalog` | ❌ Forbidden (403) | ✅ Allowed | ❌ Denied (403) |
| `PUT /api/v1/admin/users/{id}/role` | ❌ Forbidden (403) | ✅ Allowed | ❌ Denied (403) |

---

## 3. Privilege Escalation Prevention
1. **Default Registration State:** Self-service registration (`POST /api/v1/auth/register`) strictly assigns `role = UserRole.CUSTOMER` and `state = AccountState.ACTIVE`. It is impossible for a user to register themselves as `ADMIN`.
2. **Role Modification Endpoint:** Changing a user's role (`PUT /api/v1/admin/users/{id}/role`) requires the `require_admin` dependency.
3. **Suspended User Enforcement:** `get_current_user` inspects `user.state` and `user.role`. If either is `SUSPENDED`, access is terminated immediately with `HTTP 403 Forbidden`.

---

## 4. Audit Logging & Server-Side Timestamping
- **Audit Logging Table (`audit_logs`):** Administrative actions (role changes, user suspensions, user reactivations) write immutable audit log records via `AuditLogModel` detailing `actor_id`, `action`, `target_user_id`, and UTC timestamp.
- **Server Timestamp Invariant:** Order creation timestamps (`created_at`) and trade executions use server-side UTC timestamps (`datetime.now(timezone.utc)`). Client timestamps are ignored.

---

## 5. Security Audit Verification Tests

| Test Function | Location | Verified Invariant | Status |
|---|---|---|---|
| `test_customer_cannot_access_admin_endpoints` | `tests/integration/test_user_management.py` | CUSTOMER accessing admin routes receives HTTP 403. | **PASSED** |
| `test_suspended_user_cannot_access_protected_actions` | `tests/integration/test_user_management.py` | SUSPENDED user receives HTTP 403 on all protected endpoints. | **PASSED** |
| `test_unauthorized_order_access_api` | `tests/integration/test_order_api.py` | Customer A cannot cancel Customer B's orders (HTTP 403). | **PASSED** |
| `test_cross_customer_watchlist_isolation_api` | `tests/integration/test_watchlist_api.py` | Customer A cannot modify Customer B's watchlists. | **PASSED** |
| `test_ac_03_customer_denied_admin_catalog_actions_api` | `tests/integration/test_stock_catalog.py` | Customer modifying catalog receives HTTP 403. | **PASSED** |
