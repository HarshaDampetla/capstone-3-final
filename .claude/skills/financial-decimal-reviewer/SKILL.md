---
name: financial-decimal-reviewer
description: Reviews Python code paths to ensure zero floating-point arithmetic is used for financial calculations.
---

# Financial Decimal Reviewer Skill

## Purpose & Usage
Use this skill to inspect python files for improper `float` usages in financial calculations (NFR-01 compliance).

## Checklist
- Verify monetary Pydantic schema fields use `Decimal`.
- Verify database columns use `Numeric(18, 4)`.
- Verify domain policy calculations use `Decimal` with explicit rounding.
