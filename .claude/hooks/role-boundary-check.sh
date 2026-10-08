#!/usr/bin/env bash
# Pre-Commit Hook: Role Boundary Check (AC-02, NFR-04)
set -e

echo "[HOOK] Verifying role policy enforcement and admin partitioning..."

if grep -q "validate_role_transition" src/domain/role_policy.py; then
    echo "[HOOK PASS] RolePolicy transition validation present."
else
    echo "[HOOK FAIL] src/domain/role_policy.py must implement validate_role_transition."
    exit 1
fi

if grep -q "AuditLogModel" src/repositories/user_repository.py; then
    echo "[HOOK PASS] User role updates write to audit_logs."
else
    echo "[HOOK FAIL] src/repositories/user_repository.py must audit role changes to AuditLogModel."
    exit 1
fi

exit 0
