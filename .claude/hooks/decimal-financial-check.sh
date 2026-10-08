#!/usr/bin/env bash
# Pre-Commit Hook: Fixed-Point Decimal Financial Check (NFR-01)
set -e

echo "[HOOK] Verifying zero float usage in financial domain logic..."

if grep -rn "float(" src/domain/pnl_calculator.py 2>/dev/null; then
    echo "[HOOK FAIL] Float usage detected in PnLCalculator! Must use Decimal exclusively."
    exit 1
fi

if grep -rn "float(" src/domain/order_policy.py 2>/dev/null; then
    echo "[HOOK FAIL] Float usage detected in OrderPolicy! Must use Decimal exclusively."
    exit 1
fi

echo "[HOOK PASS] Financial domain policies use Python Decimal exclusively."
exit 0
