---
name: rbac-reviewer
description: Audits role-based access control and admin auditing features.
---

# RBAC Reviewer Skill

## Purpose & Usage
Use this skill to audit role partitioning (`CUSTOMER`, `ADMIN`, `SUSPENDED`) and audit trail logging (AC-02, NFR-04).

## Checklist
- Verify administrative endpoints enforce `ADMIN` role.
- Verify role modifications emit audit records in `audit_logs`.
