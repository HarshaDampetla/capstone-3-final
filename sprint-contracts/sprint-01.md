# Sprint Contract — Sprint 01: Project Foundation & User Security

**Sprint Goal:** Repository Foundation, AI-Native Substrate, & User Management (AC-01, AC-02)  
**Business Case:** BC-AINE-006  
**Status:** COMPLETED & VERIFIED  

---

## 1. Scope & Deliverables
- Setup layered directory structure (`src/api`, `src/services`, `src/domain`, `src/repositories`, `src/db`).
- Author layered `CLAUDE.md` hierarchy and `AGENTS.md` registry.
- Implement `AC-01`: Customer registration (`ACTIVE` state, `CUSTOMER` role, bcrypt hash).
- Implement `AC-02`: Admin role management (`CUSTOMER`/`ADMIN`/`SUSPENDED`) & audit logging.

---

## 2. Invariants & Acceptance Criteria
- **AC-01 Invariant:** Passwords hashed using `bcrypt` with 72-byte safety slicing. No plain passwords logged.
- **AC-02 Invariant:** `require_admin` dependency restricts admin role updates (`PUT /api/v1/admin/users/{id}/role`). Suspended users blocked (`HTTP 403`).

---

## 3. Sprint 01 Evaluation & Evidence
- **Tests Passed:** `test_ac_01_customer_registration`, `test_ac_02_admin_role_change`, `test_duplicate_registration_fails`.
- **Import Linter Status:** 2 contracts kept (`Layered Architecture Contract`, `Domain Isolation Contract`).
