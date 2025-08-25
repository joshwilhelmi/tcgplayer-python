# TCGplayer Client - Comprehensive Testing Guide

## 🧪 **Testing Overview**

This guide covers all testing aspects of the TCGplayer Client library, from unit
tests to security scanning. The project maintains high testing standards to
ensure code quality, security, and reliability.

## 📊 **Current Test Status**

- **Test Coverage**: 52% (575/1,103 lines)
- **Target Coverage**: 80%+ for production quality
- **Test Count**: 90 tests, all passing
- **Test Categories**: Authentication, API endpoints, caching, rate limiting,
error handling

## 🚀 **Quick Start Testing**

### **Run All Tests**

```bash

# Basic test run

pytest

# With coverage reporting

pytest --cov=tcgplayer_client --cov-report=html --cov-report=term-missing

# Parallel execution

pytest -n auto --dist=loadfile

```

### **Install Testing Dependencies**

```bash

# Install development dependencies

pip install -e ".[dev]"

# Install additional testing tools

pip install pytest-cov pytest-asyncio pytest-xdist
pip install memory-profiler pytest-benchmark

```

## 🧩 **Test Categories**

### **1. Unit Testing (pytest)**

#### **Core Client Tests**

```bash

# Main client functionality

pytest tests/test_client.py -v

# Authentication system

pytest tests/test_auth.py -v

# Rate limiting

pytest tests/test_rate_limiter.py -v

# Caching system

pytest tests/test_cache.py -v

```

#### **API Endpoint Tests**

```bash

# Catalog endpoints

pytest tests/test_endpoints_catalog.py -v

# Pricing endpoints

pytest tests/test_endpoints_pricing.py -v

# Store endpoints

pytest tests/test_endpoints_stores.py -v

# All endpoint tests

pytest tests/test_endpoints/ -v

```

#### **Utility Tests**

```bash

# Configuration management

pytest tests/test_config.py -v

# Input validation

pytest tests/test_validation.py -v

# Exception handling

pytest tests/test_exceptions.py -v

# Logging configuration

pytest tests/test_logging_config.py -v

```

### **2. Security Testing**

#### **Bandit Security Scanner**

```bash

# Basic security scan

bandit -r tcgplayer_client/ -f txt

# JSON output for CI/CD

bandit -r tcgplayer_client/ -f json -o bandit-report.json

# Include low confidence issues

bandit -r tcgplayer_client/ -f txt -i -ll

```

#### **Dependency Security**

```bash

# Safety vulnerability checker

safety check

# JSON output

safety check --json --output safety-report.json

# Pip audit

pip-audit --desc

# JSON output

pip-audit --desc --format=json --output=pip-audit-report.json

```

#### **Advanced Security Analysis**

```bash

# Semgrep static analysis

semgrep --config=auto tcgplayer_client/

# JSON output

semgrep --config=auto --json --output=semgrep-report.json tcgplayer_client/

# TruffleHog secret detection (for local testing)

trufflehog --only-verified .

```

### **3. Code Quality Testing**

#### **Code Formatting**

```bash

# Check Black formatting

black --check --diff .

# Apply formatting

black .

# Check import sorting

isort --check-only --diff .

# Apply import sorting

isort .

```

#### **Linting & Type Checking**

```bash

# Flake8 linting

flake8 tcgplayer_client/ tests/ --max-line-length=88 --extend-ignore=E203,W503

# MyPy type checking

mypy tcgplayer_client/ --ignore-missing-imports

# Run all quality checks

pre-commit run --all-files

```

### **4. Performance Testing**

#### **Benchmark Tests**

```bash

# Run performance benchmarks

python -m pytest tests/test_performance.py -v

# Memory profiling

python -m memory_profiler tests/test_memory.py

# Async performance

python -m pytest tests/test_async_performance.py -v

```

#### **Rate Limiting Tests**

```bash

# Test rate limit compliance

python -m pytest tests/test_rate_limit_compliance.py -v

# Stress testing

python -m pytest tests/test_stress.py -v

```

### **5. Integration Testing**

#### **Real API Testing**

```bash

# Set credentials

export TCGPLAYER_CLIENT_ID="your_client_id"
export TCGPLAYER_CLIENT_SECRET="your_client_secret"

# Run integration tests

python -m pytest tests/test_integration.py -v

# Test specific endpoints

python -m pytest tests/test_integration.py::test_catalog_endpoints -v

```

#### **End-to-End Testing**

```bash

# Full workflow testing

python -m pytest tests/test_e2e.py -v

# Authentication flow

python -m pytest tests/test_auth_flow.py -v

```

## 🔧 **Test Configuration**

### **pytest.ini Configuration**

```ini

[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --tb=short
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    performance: marks tests as performance tests
    security: marks tests as security tests

```

### **Coverage Configuration**

```ini

[coverage:run]
source = tcgplayer_client
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod

```

## 📈 **Coverage Goals & Metrics**

### **Coverage Targets**

- **Overall Coverage**: 80%+ (currently 52%)
- **Critical Paths**: 100% (authentication, rate limiting, error handling)
- **New Features**: 90%+ before merge
- **Bug Fixes**: 100% coverage for fixed code

### **Critical Paths (100% Coverage Required)**

- Authentication and token management
- Rate limiting and throttling
- Error handling and exception management
- Cache key generation and management
- Input validation and sanitization

### **Coverage Reports**

```bash

# Generate HTML coverage report

pytest --cov=tcgplayer_client --cov-report=html

# Generate XML for CI/CD

pytest --cov=tcgplayer_client --cov-report=xml

# Generate both

pytest --cov=tcgplayer_client --cov-report=html --cov-report=xml
--cov-report=term-missing

```

## 🚨 **Security Testing Requirements**

### **Pre-commit Security Checks**

```bash

# Install pre-commit hooks

pre-commit install

# Run security checks

pre-commit run --all-files

# Run specific security hooks

pre-commit run bandit --all-files
pre-commit run safety --all-files

```

### **CI/CD Security Pipeline**

The project includes automated security testing in GitHub Actions:

- **Bandit**: Security vulnerability scanning
- **Safety**: Dependency vulnerability checking
- **Semgrep**: Static analysis security testing
- **pip-audit**: Dependency security auditing
- **TruffleHog**: Secret detection scanning

## 🧪 **Test Development**

### **Writing New Tests**

```python

import pytest
from tcgplayer_client import TCGPlayerClient

@pytest.mark.asyncio
async def test_new_feature():
    """Test new feature functionality."""
    client = TCGPlayerClient()
    
    # Test the feature
    result = await client.new_feature()
    
    # Assertions
    assert result is not None
    assert isinstance(result, dict)

```

### **Test Fixtures**

```python

import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_client():
    """Create a mock client for testing."""
    client = MagicMock(spec=TCGPlayerClient)
    client.base_url = "<https://api.tcgplayer.com>"
    return client

@pytest.fixture
def sample_api_response():
    """Sample API response for testing."""
    return {
        "success": True,
        "data": [{"id": 1, "name": "Test"}]
    }

```

### **Async Testing**

```python

import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_operation():
    """Test async operations."""
    client = TCGPlayerClient()
    
    # Test async operation
    result = await client.async_operation()
    
    assert result is not None

```

## 📋 **Testing Checklist**

### **Before Committing**

- [ ] All tests pass: `pytest`
- [ ] Coverage maintained or improved
- [ ] Security scan clean: `bandit -r tcgplayer_client/`
- [ ] Code quality checks pass: `black --check . && isort --check-only . &&
flake8 . && mypy .`

### **Before Merging**

- [ ] All CI/CD checks pass
- [ ] Security tests pass
- [ ] Coverage meets targets
- [ ] Integration tests pass
- [ ] Performance tests pass

### **Before Release**

- [ ] Full test suite passes
- [ ] Security scan clean
- [ ] Coverage targets met
- [ ] Performance benchmarks stable
- [ ] Integration tests with real API pass

## 🆘 **Troubleshooting**

### **Common Test Issues**

```bash

# Import errors

export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Async test failures

pytest --asyncio-mode=auto

# Coverage issues

pytest --cov=tcgplayer_client --cov-report=term-missing -v

# Memory issues

pytest --maxfail=1 --tb=short

```

### **Test Environment Setup**

```bash

# Create fresh virtual environment

python -m venv test_env
source test_env/bin/activate

# Install dependencies

pip install -e ".[dev]"
pip install -r requirements.txt

# Run tests

pytest

```

## 📚 **Additional Resources**

- **pytest Documentation**: <https://docs.pytest.org/>
- **Coverage.py**: <https://coverage.readthedocs.io/>
- **Bandit Security**: <https://bandit.readthedocs.io/>
- **Safety**: <https://pyup.io/safety/>
- **Semgrep**: <https://semgrep.dev/>
- **Pre-commit**: <https://pre-commit.com/>

---

**Note**: This testing guide ensures the TCGplayer Client maintains high quality
and security standards. All contributors should follow these testing practices
to maintain code quality and prevent regressions.
