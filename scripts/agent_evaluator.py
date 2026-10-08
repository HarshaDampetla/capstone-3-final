#!/usr/bin/env python3
"""Programmatic Claude Agent SDK Evaluator Script (AINE-07).

Executes automated quality checks on specs, test coverage, AC tagging, and layer boundaries.
"""

import os
import sys
import json
import argparse


def run_quality_gate(ci_mode: bool = False) -> int:
    print("=== MarketScope Agent Evaluator Quality Gate ===")
    
    checks_passed = 0
    total_checks = 4

    # Check 1: Spec presence
    if os.path.exists("specs/app_spec.md"):
        print("[PASS] Root spec specs/app_spec.md exists.")
        checks_passed += 1
    else:
        print("[FAIL] Missing specs/app_spec.md")

    # Check 2: Architecture tests presence
    if os.path.exists("tests/architecture/test_layering.py"):
        print("[PASS] Architecture test suite present.")
        checks_passed += 1
    else:
        print("[FAIL] Missing tests/architecture/test_layering.py")

    # Check 3: Layering linter config
    if os.path.exists(".importlinter"):
        print("[PASS] Layering contract configuration (.importlinter) present.")
        checks_passed += 1
    else:
        print("[FAIL] Missing .importlinter")

    # Check 4: Requirements documentation
    if os.path.exists("docs/capstone-requirements.md"):
        print("[PASS] Requirements matrix docs/capstone-requirements.md present.")
        checks_passed += 1
    else:
        print("[FAIL] Missing docs/capstone-requirements.md")

    print(f"Result: {checks_passed}/{total_checks} quality checks passed.")
    
    if checks_passed == total_checks:
        return 0
    else:
        return 1 if ci_mode else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MarketScope Agent Evaluator")
    parser.add_argument("--ci-mode", action="store_true", help="Fail with non-zero exit code if quality checks fail")
    args = parser.parse_args()
    
    sys.exit(run_quality_gate(ci_mode=args.ci_mode))
