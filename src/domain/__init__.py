"""Pure Domain Layer — Isolated Business Rules, Policies, and Financial Models.

IMPORTANT ARCHITECTURAL RULE:
Modules in this package MUST NOT import from src.api, src.services, src.repositories, or src.db.
Financial calculations MUST use Python Decimal exclusively (NFR-01).
"""
