# Local Testing Pipeline

This document describes how to use the local testing pipeline that mimics
exactly what GitHub Actions does, allowing you to catch issues before they reach
the CI/CD pipeline.

## 🚀 Quick Start

### 1. Install Development Dependencies

```bash

# Activate your virtual environment

source venv/bin/activate

# Install development dependencies

pip install -r requirements-dev.txt

```

### 2. Run Quick Quality Check

```bash

# Fast feedback on code quality

python scripts/quick-check.py

```

### 3. Run Full CI Pipeline

```bash

# Run all checks (formatting, linting, type checking, tests, security)

make ci

```

## 🛠️ Available Commands

### Using Makefile (Recommended)

```bash

# Code Quality

make format              # Auto-format code with Black
make format-check        # Check formatting without changes
make import-sort         # Auto-sort imports with isort
make import-sort-check   # Check import sorting without changes
make lint                # Run Flake8 linting
make type-check          # Run MyPy type checking

# Testing

make test                # Run all tests
make test-cov            # Run tests with coverage report
make test-fast           # Run tests without coverage (faster)

# Security Scanning

make security            # Run all security tools
make bandit              # Run Bandit security scanning
make semgrep             # Run Semgrep static analysis

# Full Pipeline

make ci                  # Run complete CI pipeline
make pre-commit          # Run pre-commit checks
make fix                 # Auto-fix formatting issues

```

### Using Python Scripts

```bash

# Quick quality check

python scripts/quick-check.py

# Full local CI pipeline

python scripts/local-ci.py

# Bash script alternative

./scripts/local-ci.sh

```

## 🔍 What Each Tool Does

### Code Quality Tools

- **Black**: Code formatting (88 character line length)
- **isort**: Import sorting and organization
- **Flake8**: Linting and style checking
- **MyPy**: Static type checking

### Security Tools

- **Bandit**: Security vulnerability scanning
- **Semgrep**: Advanced static analysis
- **Safety**: Dependency vulnerability checking (optional)
- **pip-audit**: Dependency security auditing (optional)

### Testing

- **pytest**: Test framework with coverage reporting
- **pytest-cov**: Coverage measurement and reporting

## 📋 Pre-commit Workflow

### Before Every Commit

1. **Quick Check** (fast feedback):

   ```bash

   python scripts/quick-check.py

   ```

2. **Full Validation** (before pushing):

   ```bash

   make ci

   ```

3. **Auto-fix Issues** (if needed):

   ```bash

   make fix

   ```

## 🚨 Common Issues and Solutions

### Black Formatting Issues

```bash

# Auto-fix formatting

make format

# Check what would be changed

make format-check

```

### Import Sorting Issues

```bash

# Auto-fix import sorting

make import-sort

# Check what would be changed

make import-sort-check

```

### Missing Tools

If you get errors about missing tools:

```bash

# Install all development dependencies

pip install -r requirements-dev.txt

# Or install specific tools

pip install black flake8 isort mypy pytest bandit

```

### Dependency Conflicts

Some tools may have version conflicts. The pipeline is designed to handle
missing tools gracefully:

- **Safety**: Optional dependency vulnerability checker
- **Semgrep**: Advanced static analysis (installed by default)
- **pip-audit**: Optional dependency security auditor

## 🔧 Configuration Files

- **`.bandit`**: Bandit security scanning configuration
- **`.flake8`**: Flake8 linting configuration
- **`pyproject.toml`**: Black and isort configuration
- **`pytest.ini`**: Pytest configuration
- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration

## 📊 GitHub Actions vs Local Pipeline

| Check | GitHub Actions | Local Pipeline | Command |
|-------|----------------|----------------|---------|
| Black Formatting | ✅ | ✅ | `make format-check` |
| isort Import Sorting | ✅ | ✅ | `make import-sort-check` |
| Flake8 Linting | ✅ | ✅ | `make lint` |
| MyPy Type Checking | ✅ | ✅ | `make type-check` |
| Test Suite | ✅ | ✅ | `make test` |
| Bandit Security | ✅ | ✅ | `make bandit` |
| Semgrep Analysis | ✅ | ✅ | `make semgrep` |
| Build Check | ✅ | ✅ | `make build` |

## 🎯 Best Practices

1. **Run quick checks frequently** during development
2. **Run full CI before committing** to catch all issues
3. **Use `make fix`** to auto-resolve formatting issues
4. **Keep dependencies updated** to avoid version conflicts
5. **Check the output** of each tool to understand issues

## 🆘 Troubleshooting

### Virtual Environment Issues

```bash

# Ensure virtual environment is activated

source venv/bin/activate

# Check Python version

python --version

# Verify pip is working

pip list

```

### Permission Issues

```bash

# Make scripts executable

chmod +x scripts/*.sh
chmod +x scripts/*.py

```

### Tool Not Found Errors

```bash

# Install missing tools

pip install <tool-name>

# Or install all development dependencies

pip install -r requirements-dev.txt

```

## 📚 Additional Resources

- [Black Documentation](<https://black.readthedocs.io/)>
- [isort Documentation](<https://pycqa.github.io/isort/)>
- [Flake8 Documentation](<https://flake8.pycqa.org/)>
- [MyPy Documentation](<https://mypy.readthedocs.io/)>
- [Bandit Documentation](<https://bandit.readthedocs.io/)>
- [Semgrep Documentation](<https://semgrep.dev/docs/)>
- [pytest Documentation](<https://docs.pytest.org/)>

---

**Remember**: The goal is to catch issues locally before they reach GitHub
Actions. Run `make ci` before every commit to ensure your code is ready for the
CI/CD pipeline!
