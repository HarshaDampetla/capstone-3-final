---
name: order-lifecycle-validator
description: Validates order state machine transitions, BUY funds checks with Decimal, and post-execution order immutability.
---

# Order Lifecycle Validator Skill

## Purpose & Usage
Use this skill when implementing or validating trade order placement (`BUY`/`SELL`), order state machine transitions (`PENDING` → `EXECUTED` / `CANCELLED` / `REJECTED`), or verifying post-execution order immutability.

## Rules & Step-by-Step Instructions

1. **State Transition Rules (AC-07):**
   - Initial status must be `PENDING` with a server-side timestamp (AC-06).
   - `PENDING` orders may transition ONLY to `EXECUTED`, `CANCELLED`, or `REJECTED`.
   - Transitions from `EXECUTED`, `CANCELLED`, or `REJECTED` to any state are ILLEGAL and must raise `InvalidOrderStateException`.

2. **Funds Check Rules (AC-08):**
   - For `BUY` orders, calculate total cost: `total_cost = Decimal(quote_price) * Decimal(quantity)`.
   - Compare `total_cost` against `Decimal(available_cash)`.
   - If `total_cost > available_cash`, raise `InsufficientFundsException`. Zero floating-point allowed.

3. **Immutability Enforcement (NFR-02):**
   - Once an order reaches `EXECUTED` status, its quantity, quote_price, symbol, and side become IMMUTABLE.
   - Any attempt to UPDATE or DELETE an executed order must be blocked by domain policies and DB constraints.

## Verification Command
```bash
pytest tests/unit/test_order_policy.py -v
```
