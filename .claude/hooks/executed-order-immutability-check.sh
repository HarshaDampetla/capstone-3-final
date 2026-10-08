#!/usr/bin/env bash
# Pre-Commit Hook: Order Immutability Check (AC-07, NFR-02)
set -e

echo "[HOOK] Verifying post-execution order immutability policy..."

if grep -q "OrderStatus.EXECUTED: set()" src/domain/order_policy.py; then
    echo "[HOOK PASS] OrderPolicy enforces empty transition set for EXECUTED orders."
else
    echo "[HOOK FAIL] OrderPolicy must block state transitions from EXECUTED orders."
    exit 1
fi

exit 0
