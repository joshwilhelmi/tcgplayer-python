#!/usr/bin/env python3
"""
TCGplayer Client - Quick Check Script
Fast feedback on code quality before running full CI.
"""

import subprocess
import sys
from pathlib import Path


def run_quick_check() -> None:
    """Run quick formatting and linting checks."""
    print("🔍 Quick Code Quality Check")
    print("============================")
    print()

    checks = [
        ("Black formatting", ["black", "--check", "."]),
        ("isort import sorting", ["isort", "--check-only", "."]),
        (
            "Flake8 linting",
            [
                "flake8",
                "tcgplayer_client/",
                "tests/",
                "--max-line-length=88",
                "--extend-ignore=E203,W503",
            ],
        ),
    ]

    all_passed = True

    for name, command in checks:
        print(f"Checking {name}...", end=" ")
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ PASSED")
            else:
                print("❌ FAILED")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                all_passed = False
        except FileNotFoundError:
            print("⚠️  SKIPPED (tool not found)")

    print()
    if all_passed:
        print("🎉 All quick checks passed!")
        print("Run 'make ci' or 'scripts/local-ci.py' for full validation.")
    else:
        print("❌ Some checks failed. Fix the issues above before committing.")
        print("Run 'make fix' to auto-fix formatting issues.")


if __name__ == "__main__":
    run_quick_check()
