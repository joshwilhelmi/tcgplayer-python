#!/usr/bin/env python3
"""
TCGplayer Client - Release Script
Automates the release process and ensures everything is ready before publishing.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


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


def run_command(command: list[str], description: str, check: bool = True) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        if result.returncode == 0:
            return True
        else:
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print_error(f"Command not found: {' '.join(command)}")
        return False


def get_current_version() -> Optional[str]:
    """Get the current version from __init__.py."""
    init_file = Path("tcgplayer_client/__init__.py")
    if not init_file.exists():
        return None

    try:
        content = init_file.read_text()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    except Exception:
        pass

    return None


def check_git_status() -> bool:
    """Check if git repository is clean."""
    print_status("Checking git status...")

    # Check if there are uncommitted changes
    if not run_command(
        ["git", "diff-index", "--quiet", "HEAD", "--"], "Git status check"
    ):
        print_error(
            "Git repository has uncommitted changes. Please commit or stash them first."
        )
        return False

    # Check if we're on main branch
    result = subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    )
    current_branch = result.stdout.strip()

    if current_branch != "main":
        print_warning(f"Current branch is '{current_branch}', not 'main'")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != "y":
            return False

    print_success("Git repository is clean")
    return True


def run_pre_release_checks() -> bool:
    """Run all pre-release checks."""
    print_status("Running pre-release checks...")

    # Run full CI pipeline
    if not run_command(["make", "ci"], "Full CI pipeline"):
        print_error("CI pipeline failed. Please fix all issues before releasing.")
        return False

    print_success("All pre-release checks passed")
    return True


def build_package() -> bool:
    """Build the package."""
    print_status("Building package...")

    if not run_command(["make", "build"], "Package build"):
        print_error("Package build failed.")
        return False

    print_success("Package built successfully")
    return True


def create_release_tag(version: str) -> bool:
    """Create and push a release tag."""
    print_status(f"Creating release tag v{version}...")

    # Create tag
    if not run_command(["git", "tag", f"v{version}"], "Create git tag"):
        print_error("Failed to create git tag.")
        return False

    # Push tag
    if not run_command(["git", "push", "origin", f"v{version}"], "Push git tag"):
        print_error("Failed to push git tag.")
        return False

    print_success(f"Release tag v{version} created and pushed")
    return True


def main() -> None:
    """Main release function."""
    print("🚀 TCGplayer Client - Release Script")
    print("=====================================")
    print()

    # Get current version
    current_version = get_current_version()
    if not current_version:
        print_error("Could not determine current version from __init__.py")
        sys.exit(1)

    print_status(f"Current version: {current_version}")

    # Confirm release
    print(f"\n📋 About to release version {current_version}")
    print("This will:")
    print("  1. Run full CI pipeline")
    print("  2. Build the package")
    print("  3. Create git tag v{current_version}")
    print("  4. Push tag to trigger GitHub Actions")
    print("  5. Automatically publish to PyPI")
    print()

    response = input(f"Proceed with release v{current_version}? (y/N): ")
    if response.lower() != "y":
        print("Release cancelled.")
        sys.exit(0)

    # Run all checks
    if not check_git_status():
        sys.exit(1)

    if not run_pre_release_checks():
        sys.exit(1)

    if not build_package():
        sys.exit(1)

    # Create release tag
    if not create_release_tag(current_version):
        sys.exit(1)

    print()
    print("🎉 Release process completed successfully!")
    print()
    print("📋 What happens next:")
    print("  1. GitHub Actions will automatically run the publish workflow")
    print("  2. Package will be published to PyPI")
    print("  3. GitHub Release will be created")
    print()
    print("🔍 Monitor progress:")
    print(f"  GitHub Actions: https://github.com/joshwilhelmi/tcgplayer-python/actions")
    print(f"  PyPI: https://pypi.org/project/tcgplayer-client/")
    print()
    print("✅ Your package is now being published to PyPI!")


if __name__ == "__main__":
    main()
