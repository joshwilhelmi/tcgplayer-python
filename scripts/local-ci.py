#!/usr/bin/env python3
"""
TCGplayer Client - Local CI Pipeline
This script mimics the GitHub Actions pipeline exactly.
Run this before committing to catch issues early.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple


# Colors for output
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def print_status(message: str) -> None:
    """Print a status message."""
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")


def run_command(command: List[str], description: str, check: bool = True) -> bool:
    """Run a command and return success status."""
    print_status(f"Running {description}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        if result.returncode == 0:
            print_success(f"{description} passed")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print_error(f"{description} failed")
            if result.stderr:
                print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed with error: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print_warning(f"Command not found: {' '.join(command)}")
        return False


def check_python_version() -> None:
    """Check Python version."""
    print_status("Checking Python version...")
    version = sys.version_info
    print_success(f"Python version: {version.major}.{version.minor}.{version.micro}")


def install_dependencies() -> None:
    """Install development dependencies."""
    print_status("Installing development dependencies...")

    # Check if virtual environment is activated
    if not os.getenv("VIRTUAL_ENV"):
        print_warning(
            "Virtual environment not detected. Please activate your venv first."
        )
        print_status("You can activate it with: source venv/bin/activate")
        sys.exit(1)

    # Install requirements-dev.txt if it exists
    if Path("requirements-dev.txt").exists():
        if run_command(
            [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"],
            "Installing development dependencies",
        ):
            print_success("Development dependencies installed")
        else:
            print_error("Failed to install development dependencies")
            sys.exit(1)
    else:
        print_warning("requirements-dev.txt not found, installing common dev tools...")
        common_tools = [
            "black",
            "flake8",
            "isort",
            "mypy",
            "pytest",
            "pytest-cov",
            "bandit",
            "safety",
            "semgrep",
            "pip-audit",
        ]
        for tool in common_tools:
            run_command(
                [sys.executable, "-m", "pip", "install", tool],
                f"Installing {tool}",
                check=False,
            )


def run_formatting_checks() -> None:
    """Run code formatting checks."""
    print_status("Running code formatting checks...")

    # Black formatting check
    if not run_command(["black", "--check", "--diff", "."], "Black formatting check"):
        print_error("Black formatting check failed. Run 'make format' to fix.")
        sys.exit(1)

    # isort import sorting check
    if not run_command(
        ["isort", "--check-only", "--diff", "."], "isort import sorting check"
    ):
        print_error("isort import sorting check failed. Run 'make import-sort' to fix.")
        sys.exit(1)


def run_linting_checks() -> None:
    """Run linting checks."""
    print_status("Running linting checks...")

    # Flake8 linting
    flake8_cmd = [
        "flake8",
        "tcgplayer_client/",
        "tests/",
        "--max-line-length=88",
        "--extend-ignore=E203,W503",
    ]
    if not run_command(flake8_cmd, "Flake8 linting"):
        print_error("Flake8 linting failed. Please fix the issues above.")
        sys.exit(1)


def run_type_checks() -> None:
    """Run type checks."""
    print_status("Running type checks...")

    # MyPy type checking
    mypy_cmd = [
        "mypy",
        "tcgplayer_client/",
        "--ignore-missing-imports",
        "--no-strict-optional",
    ]
    if not run_command(mypy_cmd, "MyPy type checking"):
        print_error("MyPy type checking failed. Please fix the type issues above.")
        sys.exit(1)


def run_security_checks() -> None:
    """Run security checks."""
    print_status("Running security checks...")

    # Bandit security scanning
    if Path(".bandit").exists():
        if not run_command(
            ["bandit", "-c", ".bandit", "-r", "tcgplayer_client/", "-f", "txt"],
            "Bandit security scanning",
        ):
            print_error(
                "Bandit security scanning failed. Please fix the security issues above."
            )
            sys.exit(1)
    else:
        print_warning(".bandit configuration not found, skipping Bandit check")

    # Safety dependency vulnerability checker
    if run_command(
        ["safety", "check"], "Safety dependency vulnerability checker", check=False
    ):
        print_success("Safety dependency vulnerability checker passed")
    else:
        print_warning(
            "Safety found some dependency vulnerabilities. Consider updating packages."
        )

    # Semgrep static analysis
    if run_command(
        [sys.executable, "-m", "semgrep", "--config=auto", "tcgplayer_client/"],
        "Semgrep static analysis",
        check=False,
    ):
        print_success("Semgrep static analysis passed")
    else:
        print_warning("Semgrep found some issues. Please review the output above.")

    # pip-audit dependency security
    if run_command(["pip-audit"], "pip-audit dependency security check", check=False):
        print_success("pip-audit dependency security check passed")
    else:
        print_warning(
            "pip-audit found some dependency security issues. Consider updating packages."
        )


def run_tests() -> None:
    """Run tests."""
    print_status("Running tests...")

    # Run pytest
    if not run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        "pytest test suite",
    ):
        print_error("Some tests failed. Please fix the test issues above.")
        sys.exit(1)


def run_build_check() -> None:
    """Run build check."""
    print_status("Running build check...")

    # Check if package can be built
    if not run_command(
        [sys.executable, "-m", "build", "--dry-run"], "Package build check"
    ):
        print_error("Package build check failed. Please fix the build issues above.")
        sys.exit(1)


def main() -> None:
    """Main execution function."""
    print("🚀 TCGplayer Client - Local CI Pipeline")
    print("========================================")
    print()

    # Check Python version
    check_python_version()

    # Install dependencies
    install_dependencies()

    print()
    print("🔍 Running all CI checks...")
    print()

    # Run all checks
    run_formatting_checks()
    run_linting_checks()
    run_type_checks()
    run_security_checks()
    run_tests()
    run_build_check()

    print()
    print("🎉 All CI checks passed! 🎉")
    print("Your code is ready to commit and push to GitHub.")
    print()
    print("Next steps:")
    print("  git add .")
    print("  git commit -m 'Your commit message'")
    print("  git push origin main")


if __name__ == "__main__":
    main()
