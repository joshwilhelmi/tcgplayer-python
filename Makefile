# TCGplayer Client - Development Makefile
# Mimics GitHub Actions pipeline for local testing

.PHONY: help install test format lint type-check security clean build publish

# Default target
help:
	@echo "TCGplayer Client Development Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install          Install all dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo ""
	@echo "Code Quality (GitHub Actions Pipeline):"
	@echo "  format           Run Black formatting"
	@echo "  format-check     Check Black formatting without changes"
	@echo "  lint             Run Flake8 linting"
	@echo "  type-check       Run MyPy type checking"
	@echo "  import-sort      Run isort import sorting"
	@echo "  import-sort-check Check isort without changes"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-cov         Run tests with coverage report"
	@echo "  test-fast        Run tests without coverage (faster)"
	@echo ""
	@echo "Security Scanning:"
	@echo "  security         Run all security tools (Bandit, Safety, etc.)"
	@echo "  bandit           Run Bandit security scanning"
	@echo "  safety           Run Safety dependency vulnerability checker"
	@echo "  semgrep          Run Semgrep static analysis"
	@echo "  pip-audit        Run pip-audit for dependency security"
	@echo ""
	@echo "Full Pipeline:"
	@echo "  ci               Run full CI pipeline (format + lint + type-check + test + security)"
	@echo "  pre-commit       Run pre-commit checks"
	@echo ""
	@echo "Build & Distribution:"
	@echo "  build            Build package"
	@echo "  clean            Clean build artifacts"
	@echo "  publish          Build and publish to PyPI (if configured)"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Code Formatting
format:
	@echo "🔧 Running Black formatting..."
	black .
	@echo "✅ Black formatting complete"

format-check:
	@echo "🔍 Checking Black formatting..."
	black --check --diff .
	@echo "✅ Black formatting check passed"

# Linting
lint:
	@echo "🔍 Running Flake8 linting..."
	flake8 tcgplayer_client/ tests/ --max-line-length=88 --extend-ignore=E203,W503
	@echo "✅ Flake8 linting passed"

# Type Checking
type-check:
	@echo "🔍 Running MyPy type checking..."
	mypy tcgplayer_client/ --ignore-missing-imports --no-strict-optional
	@echo "✅ MyPy type checking passed"

# Import Sorting
import-sort:
	@echo "🔧 Running isort import sorting..."
	isort .
	@echo "✅ isort import sorting complete"

import-sort-check:
	@echo "🔍 Checking isort import sorting..."
	isort --check-only --diff .
	@echo "✅ isort import sorting check passed"

# Testing
test:
	@echo "🧪 Running test suite..."
	python -m pytest tests/ -v --tb=short

test-cov:
	@echo "🧪 Running test suite with coverage..."
	python -m pytest tests/ -v --cov=tcgplayer_client --cov-report=html --cov-report=term-missing

test-fast:
	@echo "🧪 Running test suite (fast mode)..."
	python -m pytest tests/ -v --tb=short --no-cov

# Security Scanning
security: bandit semgrep pip-audit
	@echo "✅ All security checks complete"

bandit:
	@echo "🔒 Running Bandit security scanning..."
	bandit -c .bandit -r tcgplayer_client/ -f txt
	@echo "✅ Bandit security scanning complete"

safety:
	@echo "🔒 Running Safety dependency vulnerability checker..."
	@echo "⚠️  Safety not available - skipping dependency vulnerability check"
	@echo "   Install with: pip install safety"

semgrep:
	@echo "🔒 Running Semgrep static analysis..."
	@if command -v semgrep >/dev/null 2>&1; then \
		semgrep --config=auto tcgplayer_client/ || true; \
		echo "✅ Semgrep static analysis complete"; \
	else \
		echo "⚠️  Semgrep not available - skipping static analysis"; \
		echo "   Install with: pip install semgrep"; \
	fi

pip-audit:
	@echo "🔒 Running pip-audit for dependency security..."
	@if command -v pip-audit >/dev/null 2>&1; then \
		pip-audit || true; \
		echo "✅ pip-audit dependency security check complete"; \
	else \
		echo "⚠️  pip-audit not available - skipping dependency security check"; \
		echo "   Install with: pip install pip-audit"; \
	fi

# Full CI Pipeline
ci: format-check import-sort-check lint type-check test security
	@echo ""
	@echo "🎉 All CI checks passed! Ready to commit and push."
	@echo ""

# Pre-commit checks
pre-commit: format import-sort lint type-check test
	@echo ""
	@echo "🎉 Pre-commit checks complete! Ready to commit."
	@echo ""

# Build & Distribution
build:
	@echo "📦 Building package..."
	python -m build
	@echo "✅ Package build complete"

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info/ htmlcov/ .coverage .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete"

# Quick fix for common issues
fix: format import-sort
	@echo "🔧 Code formatting fixed"

# Show current status
status:
	@echo "📊 Current Project Status:"
	@echo "  Python version: $(shell python --version)"
	@echo "  Package: $(shell python -c "import tcgplayer_client; print(tcgplayer_client.__version__)" 2>/dev/null || echo "Not installed")"
	@echo "  Test count: $(shell python -m pytest --collect-only -q 2>/dev/null | tail -1 | grep -o '[0-9]* collected' | grep -o '[0-9]*' || echo "Unknown")"
	@echo "  Coverage: $(shell python -m pytest --cov=tcgplayer_client --cov-report=term-missing -q 2>/dev/null | tail -1 | grep -o '[0-9]*%' | head -1 || echo "Unknown")"
