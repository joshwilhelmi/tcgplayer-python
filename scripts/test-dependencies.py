#!/usr/bin/env python3
"""
Dependency Test Runner

Run this script before commits to ensure all Python dependencies are working correctly.
This prevents CI/CD failures due to dependency issues.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   Stdout: {e.stdout}")
        if e.stderr:
            print(f"   Stderr: {e.stderr}")
        return False


def test_python_environment():
    """Test basic Python environment."""
    print("🐍 Testing Python Environment")
    print("=" * 40)

    # Test Python version
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")

    if version.major != 3 or version.minor < 8:
        print("❌ Python 3.8+ required")
        return False

    print("✅ Python version compatible")
    return True


def test_build_dependencies():
    """Test build system dependencies."""
    print("\n🔨 Testing Build Dependencies")
    print("=" * 40)

    tests = [
        (
            ["python", "-c", "import setuptools; print('setuptools available')"],
            "setuptools import",
        ),
        (["python", "-c", "import wheel; print('wheel available')"], "wheel import"),
        (["python", "-c", "import build; print('build available')"], "build import"),
    ]

    results = []
    for command, description in tests:
        results.append(run_command(command, description))

    return all(results)


def test_pyproject_toml():
    """Test pyproject.toml configuration."""
    print("\n📋 Testing pyproject.toml")
    print("=" * 40)

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return False

    # Test TOML parsing
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("❌ tomllib/tomli not available for parsing")
            return False

    try:
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)

        # Check essential sections
        required_sections = ["build-system", "project"]
        for section in required_sections:
            if section not in config:
                print(f"❌ Missing section: {section}")
                return False

        # Check project metadata
        project = config["project"]
        required_fields = ["name", "version", "description", "authors"]
        for field in required_fields:
            if field not in project:
                print(f"❌ Missing field: project.{field}")
                return False

        print("✅ pyproject.toml configuration valid")
        return True

    except Exception as e:
        print(f"❌ Failed to parse pyproject.toml: {e}")
        return False


def test_package_build():
    """Test package build process."""
    print("\n📦 Testing Package Build")
    print("=" * 40)

    # Clean existing builds
    dist_path = Path("dist")
    if dist_path.exists():
        import shutil

        shutil.rmtree(dist_path)
        print("🧹 Cleaned existing builds")

    # Test build
    if run_command(["python", "-m", "build"], "package build"):
        # Verify build artifacts
        if dist_path.exists():
            wheel_files = list(dist_path.glob("*.whl"))
            source_files = list(dist_path.glob("*.tar.gz"))

            if wheel_files and source_files:
                print(
                    f"✅ Build artifacts created: {len(wheel_files)} wheel(s), {len(source_files)} source(s)"
                )
                return True
            else:
                print("❌ Build artifacts incomplete")
                return False
        else:
            print("❌ Build directory not created")
            return False
    else:
        return False


def test_package_installation():
    """Test package installation."""
    print("\n⬇️  Testing Package Installation")
    print("=" * 40)

    # Test editable install
    if run_command(
        ["python", "-m", "pip", "install", "-e", "."], "editable installation"
    ):
        # Test package import
        if run_command(
            [
                "python",
                "-c",
                "import tcgplayer_client; print('Package imported successfully')",
            ],
            "package import",
        ):
            return True

    return False


def test_dependencies():
    """Test all dependencies."""
    print("\n🔗 Testing Dependencies")
    print("=" * 40)

    # Core dependencies
    core_deps = ["aiohttp"]
    core_results = []

    for dep in core_deps:
        if run_command(
            ["python", "-c", f"import {dep}; print('{dep} available')"],
            f"core dependency: {dep}",
        ):
            core_results.append(True)
        else:
            core_results.append(False)

    # Development dependencies (optional)
    dev_deps = ["pytest", "black", "flake8", "mypy"]
    dev_results = []

    for dep in dev_deps:
        try:
            result = subprocess.run(
                ["python", "-c", f"import {dep}"],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"✅ {dep} available (dev)")
            dev_results.append(True)
        except subprocess.CalledProcessError:
            print(f"⚠️  {dep} not available (dev dependency)")
            dev_results.append(False)

    # Core dependencies must all pass
    if not all(core_results):
        print("❌ Core dependencies failed")
        return False

    print("✅ All core dependencies available")
    return True


def run_full_dependency_test():
    """Run the complete dependency test suite."""
    print("🚀 Running Full Dependency Test Suite")
    print("=" * 60)

    test_results = []

    # Run all tests
    tests = [
        ("Python Environment", test_python_environment),
        ("Build Dependencies", test_build_dependencies),
        ("pyproject.toml", test_pyproject_toml),
        ("Package Build", test_package_build),
        ("Package Installation", test_package_installation),
        ("Dependencies", test_dependencies),
    ]

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            test_results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Ready to commit.")
        return True
    else:
        print("💥 Some tests failed. Fix issues before committing.")
        return False


if __name__ == "__main__":
    """Main entry point."""
    success = run_full_dependency_test()

    if success:
        print("\n🚀 Dependency tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Dependency tests failed!")
        sys.exit(1)
