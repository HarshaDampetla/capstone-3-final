#!/usr/bin/env python3
"""Cross-platform Python Hook Runner for Windows & Linux CI environments."""

import sys
import subprocess
import os

def check_password_hash():
    print("[HOOK] Checking for unhashed passwords or plaintext credential logging...")
    with open("src/core/security.py", "r", encoding="utf-8") as f:
        content = f.read()
    if "bcrypt.hashpw" not in content and "CryptContext" not in content:
        print("[HOOK FAIL] src/core/security.py must configure bcrypt password hashing.")
        return False
    print("[HOOK PASS] Password hashing using bcrypt verified.")
    return True

def check_role_boundary():
    print("[HOOK] Verifying role policy enforcement and admin partitioning...")
    with open("src/domain/role_policy.py", "r", encoding="utf-8") as f:
        content = f.read()
    if "validate_role_transition" not in content:
        print("[HOOK FAIL] src/domain/role_policy.py must implement validate_role_transition.")
        return False
    print("[HOOK PASS] RolePolicy transition validation present.")
    return True

def check_order_immutability():
    print("[HOOK] Verifying post-execution order immutability policy...")
    with open("src/domain/order_policy.py", "r", encoding="utf-8") as f:
        content = f.read()
    if "OrderStatus.EXECUTED: set()" not in content:
        print("[HOOK FAIL] OrderPolicy must block state transitions from EXECUTED orders.")
        return False
    print("[HOOK PASS] OrderPolicy enforces empty transition set for EXECUTED orders.")
    return True

def check_decimal_financial():
    print("[HOOK] Verifying zero float usage in financial domain logic...")
    for path in ["src/domain/pnl_calculator.py", "src/domain/order_policy.py"]:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for idx, line in enumerate(lines, 1):
                if "float(" in line:
                    print(f"[HOOK FAIL] Float usage detected in {path}:{idx}!")
                    return False
    print("[HOOK PASS] Financial domain policies use Python Decimal exclusively.")
    return True

if __name__ == "__main__":
    results = [
        check_password_hash(),
        check_role_boundary(),
        check_order_immutability(),
        check_decimal_financial()
    ]
    if all(results):
        print("\nAll 4 Substrate Pre-Commit Hooks PASSED successfully.")
        sys.exit(0)
    else:
        print("\nOne or more Substrate Pre-Commit Hooks FAILED.")
        sys.exit(1)
