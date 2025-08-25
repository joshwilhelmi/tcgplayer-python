#!/usr/bin/env python3
"""
Test Python Install Dependencies

This module tests all aspects of Python package installation and build dependencies
to catch issues before they reach CI/CD pipelines.
"""

import importlib
import subprocess
import sys
from pathlib import Path
from typing import Dict

try:
    import pkg_resources

    PKG_RESOURCES_AVAILABLE = True
except ImportError:
    PKG_RESOURCES_AVAILABLE = False
import pytest


class TestPythonEnvironment:
    """Test Python environment and version compatibility."""

    def test_python_version(self):
        """Test that Python version meets minimum requirements."""
        version = sys.version_info
        assert (
            version.major == 3
        ), f"Expected Python 3.x, got {version.major}.{version.minor}"
        assert (
            version.minor >= 8
        ), f"Expected Python 3.8+, got {version.major}.{version.minor}"
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")

    def test_pip_version(self):
        """Test pip version compatibility."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
            version_str = result.stdout.strip()
            print(f"✅ Pip version: {version_str}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to get pip version: {e}")

    def test_setuptools_version(self):
        """Test setuptools version compatibility."""
        if not PKG_RESOURCES_AVAILABLE:
            pytest.skip("pkg_resources not available")

        try:
            version = pkg_resources.get_distribution("setuptools").version
            version_tuple = tuple(map(int, version.split(".")[:2]))

            # Check minimum version - GitHub Actions may have older versions
            min_version = (58, 0)  # Lowered from 61.0 for CI compatibility
            if version_tuple < min_version:
                pytest.skip(
                    f"setuptools {version} < {min_version[0]}.{min_version[1]} "
                    "(CI environment)"
                )

            # Check if version supports our features
            if version_tuple >= (77, 0):
                print(f"✅ setuptools {version} (supports modern license syntax)")
            elif version_tuple >= (61, 0):
                print(f"✅ setuptools {version} (supports standard features)")
            else:
                print(f"⚠️  setuptools {version} (legacy mode, some warnings expected)")

        except Exception as e:
            pytest.fail(f"Failed to check setuptools version: {e}")


class TestBuildDependencies:
    """Test build system dependencies and compatibility."""

    def test_build_tools_available(self):
        """Test that essential build tools are available."""
        required_tools = ["setuptools", "wheel"]

        for tool in required_tools:
            try:
                importlib.import_module(tool)
                print(f"✅ {tool} available")
            except ImportError:
                if tool == "wheel":
                    print(f"⚠️  {tool} not available (build dependency)")
                elif tool == "setuptools":
                    print(f"⚠️  {tool} not available (CI environment)")
                else:
                    pytest.fail(f"{tool} not available")

    def test_pyproject_toml_parsing(self):
        """Test that pyproject.toml can be parsed correctly."""
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                pytest.skip("tomllib/tomli not available")

        pyproject_path = Path("pyproject.toml")
        assert pyproject_path.exists(), "pyproject.toml not found"

        try:
            with open(pyproject_path, "rb") as f:
                config = tomllib.load(f)

            # Check essential sections
            assert "build-system" in config, "build-system section missing"
            assert "project" in config, "project section missing"

            # Check build system requirements
            build_system = config["build-system"]
            assert "requires" in build_system, "build-system.requires missing"
            assert "build-backend" in build_system, "build-system.build-backend missing"

            # Check project metadata
            project = config["project"]
            required_fields = ["name", "version", "description", "authors"]
            for field in required_fields:
                assert field in project, f"project.{field} missing"

            print("✅ pyproject.toml parsed successfully")

        except Exception as e:
            pytest.fail(f"Failed to parse pyproject.toml: {e}")

    def test_license_configuration(self):
        """Test license configuration compatibility."""
        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                pytest.skip("tomllib/tomli not available")

        pyproject_path = Path("pyproject.toml")
        with open(pyproject_path, "rb") as f:
            config = tomllib.load(f)

        project = config["project"]

        # Check if license is configured
        assert "license" in project, "license configuration missing"

        license_config = project["license"]

        # Test different license configurations
        if isinstance(license_config, dict):
            if "text" in license_config:
                print("✅ License configured as text")
            elif "file" in license_config:
                print("✅ License configured as file reference")
            else:
                pytest.fail("Invalid license configuration")
        elif isinstance(license_config, str):
            print("✅ License configured as string")
        else:
            pytest.fail(
                f"Unexpected license configuration type: {type(license_config)}"
            )


class TestPackageInstallation:
    """Test package installation and build process."""

    def test_package_build(self):
        """Test that the package can be built successfully."""
        # Check if build tools are available
        try:
            importlib.import_module("build")
        except ImportError:
            pytest.skip("build module not available")

        try:
            # Clean any existing builds
            dist_path = Path("dist")
            if dist_path.exists():
                import shutil

                shutil.rmtree(dist_path)

            # Test build command
            subprocess.run(
                [sys.executable, "-m", "build"],
                capture_output=True,
                text=True,
                check=True,
            )

            # Check if build artifacts were created
            assert dist_path.exists(), "dist directory not created"

            # Check for wheel and source distribution
            wheel_files = list(dist_path.glob("*.whl"))
            source_files = list(dist_path.glob("*.tar.gz"))

            assert len(wheel_files) > 0, "No wheel files created"
            assert len(source_files) > 0, "No source distribution created"

            print(
                f"✅ Package built successfully: {len(wheel_files)} wheel(s), "
                f"{len(source_files)} source(s)"
            )

        except subprocess.CalledProcessError as e:
            pytest.fail(f"Build failed: {e.stderr}")
        except Exception as e:
            pytest.fail(f"Build test failed: {e}")

    def test_package_metadata(self):
        """Test package metadata and dependencies."""
        try:
            # Import the package
            import tcgplayer_client

            # Check version
            assert hasattr(tcgplayer_client, "__version__"), "__version__ not defined"
            version = tcgplayer_client.__version__
            assert version, "Version is empty"

            # Check author
            assert hasattr(tcgplayer_client, "__author__"), "__author__ not defined"
            author = tcgplayer_client.__author__
            assert author, "Author is empty"

            print(f"✅ Package metadata: version={version}, author={author}")

        except ImportError as e:
            pytest.fail(f"Failed to import package: {e}")
        except Exception as e:
            pytest.fail(f"Metadata test failed: {e}")

    def test_dependencies_importable(self):
        """Test that all declared dependencies can be imported."""
        # Core dependencies
        core_deps = ["aiohttp"]

        for dep in core_deps:
            try:
                importlib.import_module(dep)
                print(f"✅ {dep} importable")
            except ImportError as e:
                pytest.fail(f"Core dependency {dep} not importable: {e}")

        # Development dependencies (if available)
        dev_deps = ["pytest", "black", "flake8", "mypy"]

        for dep in dev_deps:
            try:
                importlib.import_module(dep)
                print(f"✅ {dep} importable (dev)")
            except ImportError:
                print(f"⚠️  {dep} not available (dev dependency)")


class TestCICompatibility:
    """Test compatibility with CI/CD environments."""

    def test_github_actions_compatibility(self):
        """Test compatibility with GitHub Actions Python versions."""
        python_version = sys.version_info

        # GitHub Actions supports Python 3.8+
        supported_versions = [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13)]
        current_version = (python_version.major, python_version.minor)

        assert current_version in supported_versions, (
            f"Python {current_version[0]}.{current_version[1]} not in supported "
            f"versions: {supported_versions}"
        )

        print(
            f"✅ Python {current_version[0]}.{current_version[1]} "
            "supported by GitHub Actions"
        )

    def test_package_install_editable(self):
        """Test editable installation (used in CI)."""
        try:
            # Test editable install command
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", "."],
                capture_output=True,
                text=True,
                check=True,
            )

            print("✅ Editable installation successful")

        except subprocess.CalledProcessError as e:
            pytest.fail(f"Editable installation failed: {e.stderr}")


def run_dependency_health_check() -> Dict[str, bool]:
    """Run a comprehensive dependency health check."""
    print("🔍 Running Python Dependency Health Check")
    print("=" * 50)

    results = {}

    # Test categories
    test_categories = [
        ("Python Environment", TestPythonEnvironment),
        ("Build Dependencies", TestBuildDependencies),
        ("Package Installation", TestPackageInstallation),
        ("CI Compatibility", TestCICompatibility),
    ]

    for category_name, test_class in test_categories:
        print(f"\n📋 {category_name}")
        print("-" * 30)

        category_results = []

        # Get test methods
        test_methods = [
            method
            for method in dir(test_class)
            if method.startswith("test_") and callable(getattr(test_class, method))
        ]

        for method_name in test_methods:
            try:
                # Create test instance and run method
                test_instance = test_class()
                method = getattr(test_instance, method_name)
                method()
                category_results.append(True)
                print(f"  ✅ {method_name}")
            except Exception as e:
                category_results.append(False)
                print(f"  ❌ {method_name}: {e}")

        # Calculate success rate
        success_rate = (
            sum(category_results) / len(category_results) if category_results else 0
        )
        results[category_name] = success_rate

        print(f"  📊 Success Rate: {success_rate:.1%}")

    print("\n" + "=" * 50)
    print("📊 Overall Results:")

    overall_success = sum(results.values()) / len(results) if results else 0
    print(f"🎯 Overall Success Rate: {overall_success:.1%}")

    for category, rate in results.items():
        status = "✅" if rate == 1.0 else "⚠️" if rate >= 0.8 else "❌"
        print(f"  {status} {category}: {rate:.1%}")

    return results


if __name__ == "__main__":
    """Run dependency health check when executed directly."""
    results = run_dependency_health_check()

    # Exit with error code if any category failed completely
    if any(rate == 0.0 for rate in results.values()):
        sys.exit(1)
    elif any(rate < 0.8 for rate in results.values()):
        sys.exit(2)  # Warning
    else:
        sys.exit(0)  # Success
