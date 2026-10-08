#!/usr/bin/env bash
# Pre-Commit Hook: Password Hashing Enforcement (NFR-03)
set -e

echo "[HOOK] Checking for unhashed passwords or plaintext credential logging..."

# Check if bcrypt is used in security core
if grep -q "bcrypt.hashpw" src/core/security.py || grep -q "CryptContext" src/core/security.py; then
    echo "[HOOK PASS] Password hashing using bcrypt verified."
else
    echo "[HOOK FAIL] src/core/security.py must configure bcrypt password hashing."
    exit 1
fi

# Check for accidental print statements logging passwords
if grep -rn "print(.*password.*)" src/ 2>/dev/null; then
    echo "[HOOK FAIL] Plaintext password logging detected in src/!"
    exit 1
else
    echo "[HOOK PASS] Zero plaintext password logging detected."
fi

exit 0
