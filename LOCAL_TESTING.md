# Local Testing Pipeline

This document describes how to use the local testing pipeline that mimics
exactly what GitHub Actions does, allowing you to catch issues before they reach
the CI/CD pipeline.

## 🚀 Quick Start

### 1. Install Development Dependencies

```bash
# Modern UV setup (10-100x faster than pip)
make install

# Or directly with UV
uv sync --all-extras
```

### 2. Run Quick Quality Check

```bash
# Fast feedback on code quality
make format lint
```

### 3. Run Full CI Pipeline

```bash
# Complete GitHub Actions pipeline locally
make ci
```

## 📋 Available Commands

### Code Quality

```bash
# Formatting and linting
make format          # Auto-format code with Black
make format-check    # Check formatting without changes
make lint            # Run Flake8 linting
make import-sort     # Fix import ordering with isort
make type-check      # Run MyPy type checking
```

### Testing

```bash
# Test execution
make test            # Run full test suite with coverage
make test-fast       # Run tests without coverage (faster)
make test-cov        # Run tests with detailed coverage report
```

### Security

```bash
# Security scanning
make security        # Run all security tools
make bandit          # Security vulnerability scanning
make semgrep         # Static analysis security scanning
make pip-audit       # Dependency vulnerability audit
```

### Build and Release

```bash
# Package management
make build           # Build distribution packages
make clean           # Clean build artifacts
make publish         # Publish to PyPI (after manual verification)
```

## 🔧 Development Workflow

### Before Every Commit

```bash
# Run the complete pipeline
make ci
```

This runs:
1. ✅ Code formatting (Black)
2. ✅ Import sorting (isort) 
3. ✅ Linting (Flake8)
4. ✅ Type checking (MyPy)
5. ✅ Security scanning (Bandit, Semgrep)
6. ✅ Full test suite
7. ✅ Build verification

### Quick Feedback Loop

```bash
# For rapid development
make format lint test-fast
```

### Fix Common Issues

```bash
# Auto-fix formatting and import issues
make fix
```

## 💡 Pro Tips

1. **Use `make ci` before every commit** - catches issues early
2. **Use `make test-fast` during development** - faster iteration
3. **Use `make fix` to auto-resolve** formatting and import issues
4. **All commands use UV** - no need to manage virtual environments manually

## 🏗️ Architecture

The local pipeline uses:
- **UV** for fast dependency management
- **Makefile** for consistent command interface  
- **Same tools as CI** ensuring identical results locally and remotely

This replaces the legacy `scripts/` directory with a modern, integrated approach.