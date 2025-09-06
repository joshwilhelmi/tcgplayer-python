# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **TCGplayer Client** - a Python client library for the TCGplayer API with async support, intelligent rate limiting, caching, and comprehensive endpoint coverage. It's a production-ready library that enforces TCGplayer's critical rate limit of **10 requests per second** to prevent API access revocation.

## Essential Commands

### Development Setup
```bash
# Install in development mode
pip install -e ".[dev]"

# Install development dependencies
make install-dev
# OR
pip install -r requirements-dev.txt
```

### Code Quality Pipeline
```bash
# Full CI pipeline (run before committing)
make ci

# Individual quality checks
make format          # Black formatting
make lint            # Flake8 linting
make type-check      # MyPy type checking
make import-sort     # isort import sorting

# Auto-fix formatting issues
make fix
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
make test-cov
# OR
pytest --cov=tcgplayer_client --cov-report=html --cov-report=term-missing

# Run specific test categories
pytest tests/test_client.py         # Main client tests
pytest tests/test_auth.py           # Authentication tests
pytest tests/test_rate_limiter.py   # Rate limiting tests
pytest tests/test_endpoints_*.py    # API endpoint tests

# Fast test run (no coverage)
make test-fast
```

### Security Scanning
```bash
# Full security scan
make security

# Individual security tools
make bandit          # Security vulnerability scanning
make semgrep         # Static analysis
make pip-audit       # Dependency security audit
```

### Build & Release
```bash
# Build package
make build

# Clean artifacts
make clean

# Release preparation
make release
```

## Code Architecture

### Core Components
- **`client.py`**: Main `TCGPlayerClient` class - entry point for all API interactions
- **`auth.py`**: OAuth2 authentication with automatic token refresh
- **`rate_limiter.py`**: Critical rate limiting (max 10 req/sec) to prevent API revocation
- **`session_manager.py`**: HTTP session management with connection pooling
- **`cache.py`**: Response caching with TTL and LRU eviction
- **`config.py`**: Configuration management with environment variable support
- **`validation.py`**: Input validation and parameter checking
- **`exceptions.py`**: Comprehensive exception hierarchy

### API Endpoints Structure
```
tcgplayer_client/endpoints/
├── catalog.py       # Product catalogs, categories, groups, search
├── pricing.py       # Market prices, price guides (NO buylist - discontinued)
├── stores.py        # Store information and inventory
├── orders.py        # Order management
└── inventory.py     # Inventory management
```

### Key Design Patterns
- **Async/Await**: All API calls are async for non-blocking I/O
- **Rate Limiting**: Enforced 10 req/sec limit with adaptive throttling
- **Caching**: Smart response caching to reduce API calls
- **Error Handling**: Detailed exception hierarchy with retry logic
- **Configuration**: Flexible config via environment variables or config objects

## Critical Rate Limiting

**⚠️ CRITICAL**: TCGplayer's API has a hard maximum of **10 requests per second**. Exceeding this can result in permanent API access revocation. The client automatically enforces this limit.

```python
# Rate limiting is automatically handled
client = TCGPlayerClient(
    max_requests_per_second=20  # Will be automatically capped to 10
)
```

## Testing Standards

- **Target Coverage**: 80%+ (currently improving from 52%)
- **Critical Path Coverage**: 100% for auth, rate limiting, error handling
- **Test Categories**: Unit, integration, security, performance
- **Security**: Automated Bandit, Semgrep, and dependency scanning

### Test Structure
- `tests/test_client.py` - Main client functionality
- `tests/test_auth.py` - Authentication flows
- `tests/test_rate_limiter.py` - Rate limiting compliance
- `tests/test_endpoints_*.py` - Individual API endpoints
- `tests/conftest.py` - Shared fixtures

## Configuration

### Environment Variables
```bash
TCGPLAYER_CLIENT_ID="your_client_id"
TCGPLAYER_CLIENT_SECRET="your_client_secret"
TCGPLAYER_LOG_LEVEL="INFO"
TCGPLAYER_ENABLE_CACHING="true"
TCGPLAYER_CACHE_TTL="300"
```

### Configuration Object
```python
from tcgplayer_client import ClientConfig

config = ClientConfig(
    max_requests_per_second=10,  # Enforced maximum
    enable_caching=True,
    cache_ttl=300,
    log_level="INFO"
)
```

## Key Dependencies

- **Python**: 3.8+ (supports 3.8-3.12)
- **aiohttp**: 3.8.0+ (async HTTP client)
- **Development**: pytest, black, flake8, mypy, bandit, semgrep

## Security Notes

- Never commit API credentials
- Security scanning integrated into CI/CD
- Fixed security issues: MD5→SHA256, proper exception handling
- Automatic secret detection in CI

## Common Development Tasks

### Adding New API Endpoints
1. Add method to appropriate endpoint class in `tcgplayer_client/endpoints/`
2. Follow existing async patterns and error handling
3. Add comprehensive tests in `tests/test_endpoints_*.py`
4. Update documentation if needed

### Debugging Rate Limiting
- Check logs for rate limit warnings
- Use `RateLimiter.get_stats()` for monitoring
- Test with `tests/test_rate_limiter.py`

### Performance Optimization
- Use caching for repeated requests
- Batch API calls when possible
- Monitor async performance with profiling tools

## Pre-commit Checklist

1. Run `make ci` (full pipeline)
2. Check coverage: `make test-cov`
3. Security scan: `make security`
4. Format code: `make format`

## Version Information

- **Current Version**: 2.0.3
- **Breaking Changes**: v2.0+ removed buylist endpoints (discontinued by TCGplayer)
- **Python Support**: 3.8-3.12
- **License**: MIT

---

## 🚨 CRITICAL: Endpoint Implementation Reconstruction

### Current Crisis
Systematic review revealed **only ~35% implementation accuracy** with critical system-wide failures across all endpoint categories. This requires immediate complete reconstruction.

### Root Cause Analysis
1. **Wrong API Documentation**: Original implementation based on incorrect/incomplete API documentation
2. **No API Spec Validation**: Endpoints built without validating against official API
3. **Parameter Type Mismatches**: Systematic confusion between IDs and keys (storeKey vs storeId)
4. **Architectural Confusion**: Functionality scattered across wrong classes
5. **Missing Endpoints**: Many endpoints incorrectly assumed discontinued

### Clean Implementation Strategy

#### Phase 1: Category-by-Category Reconstruction ✅ IN PROGRESS
Using `api-endpoints.json` as single source of truth, implementing smallest to largest:

1. **🚧 App (1 endpoint)** - Application authorization ← CURRENT
2. **⏳ Inventory (4 endpoints)** - Product list management  
3. **⏳ Pricing (7 endpoints)** - Market and buylist pricing
4. **⏳ Catalog (21 endpoints)** - Product catalog operations
5. **⏳ Stores (47 endpoints)** - Store management and operations

#### Implementation Standards
- **URL Construction**: Exact match with API documentation paths
- **Parameter Types**: Correct types (storeKey as string, not int)
- **Method Signatures**: Clear, consistent parameter naming
- **No Scope Creep**: Each endpoint class handles only its category
- **API Compliance**: 100% adherence to official TCGPlayer API spec

#### Critical Fixes Required
- **storeKey is string, not int** - affects ~25+ store endpoints
- **Buylist endpoints exist** - 3 pricing endpoints incorrectly removed
- **No /v1.39.0/ prefixes** - clean API paths only
- **Proper URL casing** - /productLists not /productlists

### Progress Tracking

#### ✅ INFRASTRUCTURE COMPLETED
- [x] Systematic endpoint review completed
- [x] Official API documentation (`api-endpoints.json`) obtained
- [x] Backup of existing code created (`backup/old_endpoints/`)
- [x] Clean implementation strategy defined

#### ✅ APP CATEGORY (1/1 endpoints) - COMPLETED
**Target**: Create proper AppEndpoints class for authorization
- [x] Extract from StoreEndpoints (architectural issue) ✅
- [x] Implement clean AppEndpoints class ✅
- [x] Create comprehensive unit tests ✅
- [x] Integration with main client ✅
- **Usage**: `client.endpoints.app.authorize_application(auth_code)`

#### ⏳ INVENTORY CATEGORY (0/4 endpoints) - UPCOMING
**Issues to Fix**: Wrong URL paths, incorrect casing, scope creep
- [ ] Fix productList vs productlist casing
- [ ] Fix wrong path for productListKey lookup
- [ ] Remove store-related scope creep (10+ methods)
- [ ] Implement missing product list management

#### ⏳ PRICING CATEGORY (0/7 endpoints) - UPCOMING  
**Issues to Fix**: Missing buylist endpoints, wrong paths
- [ ] Restore 3 buylist endpoints that were incorrectly removed
- [ ] Fix SKU market prices wrong path
- [ ] Remove duplicate methods
- [ ] Correct parameter handling

#### ⏳ CATALOG CATEGORY (0/21 endpoints) - UPCOMING
**Issues to Fix**: 8 missing endpoints (38% missing), version prefix errors
- [ ] Implement 8 missing category-specific endpoints
- [ ] Remove incorrect /v1.39.0/ version prefixes
- [ ] Fix single vs multiple ID parameter handling
- [ ] Remove non-existent endpoint calls

#### ⏳ STORES CATEGORY (0/47 endpoints) - UPCOMING
**Issues to Fix**: Wrong parameter types throughout, missing endpoints
- [ ] Fix storeKey vs storeId confusion (~25+ endpoints affected)
- [ ] Implement missing store management endpoints (~15+ missing)
- [ ] Correct URL path construction errors
- [ ] Remove architectural confusion and duplicates

### Success Criteria
- [ ] All 80 endpoints implemented correctly
- [ ] 100% URL path accuracy with API documentation
- [ ] Correct parameter types throughout
- [ ] No scope creep between endpoint categories
- [ ] All endpoints tested against live API
- [ ] Comprehensive test coverage for new implementations

### Current Status: **PHASE 1 - APP CATEGORY COMPLETED** ✅

**Progress**: 1/5 categories completed (20%)
- ✅ **App Category**: Clean AppEndpoints implementation completed
- **Usage**: Application authorization now accessible via `client.endpoints.app.authorize_application(auth_code)`
- **Architecture**: Proper separation from store-specific functionality

**Next Steps**: 
1. Move to Inventory category (4 endpoints)
2. Fix URL casing and path construction issues
3. Remove store-related scope creep