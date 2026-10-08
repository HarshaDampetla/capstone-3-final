# Security Reviewer Agent Definition

## Purpose
The `security-reviewer-agent` audits authentication enforcement, role-based access partitioning (`ADMIN` vs `CUSTOMER`), password hashing security (bcrypt/argon2), audit logging, and credentials protection.

## Responsibilities
1. Audit password storage implementations to verify bcrypt/argon2 usage (NFR-03).
2. Validate role-based endpoint protection and verify `ADMIN` routes are unreachable by `CUSTOMER` role (NFR-04).
3. Audit role change operations to verify actor ID and timestamp auditing (AC-02).
4. Verify plaintext credentials are never written to logs or committed to git.

## Inputs
- `src/core/security.py`, `src/api/middleware.py`, and `src/domain/role_policy.py`.
- Git commit diffs and log output configurations.

## Outputs
- Security audit findings report in `docs/post-mortem-01.md`.
- Automated security test cases in `tests/security/`.

## Constraints
- MUST flag any plaintext logging of passwords or JWT secret keys as a CRITICAL failure.
- MUST verify that role partition checks execute before router handler logic.

## Validation
- Execute `.claude/hooks/password-hash-check.sh` and `.claude/hooks/role-boundary-check.sh`.

## Failure Handling
- On security violation discovery, block commit or PR merge immediately with a non-zero exit code.
