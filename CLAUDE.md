# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **TCGplayer Client** - a Python client library for the TCGplayer API with async support, intelligent rate limiting, caching, and comprehensive endpoint coverage. It's a production-ready library that enforces TCGplayer's critical rate limit of **10 requests per second** to prevent API access revocation.

## Essential Commands

### Development Setup ✅ UV MODERN SETUP
```bash
# ✅ MODERN: Install with UV (10-100x faster than pip)
make install         # uv sync --all-extras
# OR
uv sync --all-extras

# 🚫 OLD: pip install -e ".[dev]" (deprecated)
```

### Code Quality Pipeline ✅ UV INTEGRATION
```bash
# Full CI pipeline (run before committing)
make ci

# Individual quality checks (now using UV)
make format          # uv run black .
make lint            # uv run flake8 tcgplayer_client/ tests/
make type-check      # uv run mypy tcgplayer_client/
make import-sort     # uv run isort .

# Auto-fix formatting issues
make fix
```

### Testing ✅ UV INTEGRATION
```bash
# Run all tests (now using UV)
make test            # uv run pytest tests/ -v

# Run tests with coverage
make test-cov        # uv run pytest --cov=tcgplayer_client

# Run specific test categories
uv run pytest tests/test_client.py         # Main client tests
uv run pytest tests/test_auth.py           # Authentication tests
uv run pytest tests/test_rate_limiter.py   # Rate limiting tests
uv run pytest tests/test_endpoints_catalog.py -v  # Catalog endpoint tests

# Fast test run (no coverage)
make test-fast       # uv run pytest tests/ -v --tb=short --no-cov
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
- **`client.py`**: Main `TCGplayerClient` class - entry point for all API interactions
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
├── pricing.py       # Market prices, buylist prices
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
client = TCGplayerClient(
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

### Environment Variables & .env File Support ✅ AUTO-LOADING
The client automatically loads credentials from `.env` files (requires `python-dotenv`):

**Create `.env` file (automatically ignored by git):**
```bash
TCGPLAYER_CLIENT_ID="your_client_id"
TCGPLAYER_CLIENT_SECRET="your_client_secret"
TCGPLAYER_LOG_LEVEL="INFO"
TCGPLAYER_ENABLE_CACHING="true"
TCGPLAYER_CACHE_TTL="300"
```

**Or set environment variables directly:**
```bash
export TCGPLAYER_CLIENT_ID="your_client_id"
export TCGPLAYER_CLIENT_SECRET="your_client_secret"
```

### Simple Usage (Automatic .env Loading)
```python
from tcgplayer_client import TCGplayerClient

# Automatically loads from .env file
async with TCGplayerClient() as client:
    await client.authenticate()
    categories = await client.endpoints.catalog.list_all_categories()
```

### Configuration Object (Advanced)
```python
from tcgplayer_client import ClientConfig

config = ClientConfig(
    client_id="your_id",  # Or loads from .env
    client_secret="your_secret",  # Or loads from .env
    max_requests_per_second=10,  # Enforced maximum
    enable_caching=True,
    cache_ttl=300,
    log_level="INFO"
)

async with TCGplayerClient(config=config) as client:
    # Your API calls here
    pass
```

## Key Dependencies

- **Python**: 3.8+ (supports 3.8-3.12)  
- **aiohttp**: 3.8.0+ (async HTTP client)
- **pywebview**: 4.0+ (OAuth automation)
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

### Endpoint Testing Format Standards

**Comprehensive Test Report Format:**
Each endpoint test in `ENDPOINT_TEST_timestamp.md` should follow this clean format:

```markdown
- **PASS/FAIL** | Friendly Endpoint Name | `method_call_with_params` | HTTP_METHOD
```

**Examples:**
```markdown
- **PASS** | List All Categories | `client.endpoints.catalog.list_all_categories()` | GET
- **FAIL** | Update SKU Price | `client.endpoints.stores.update_sku_inventory_price('3d05ef67', 1195969, 25.99, 1)` | PUT
- **PASS** | Get Market Price | `client.endpoints.pricing.get_market_price_by_sku(1195969)` | GET
```

**Required Elements:**
1. **Status**: PASS/FAIL (clear result)
2. **Friendly Name**: Human-readable endpoint description 
3. **Method Call**: Actual client method with parameters shown
4. **HTTP Method**: GET/POST/PUT/DELETE for API understanding

**Implementation Notes:**
- Use descriptive friendly names (not just API endpoint paths)
- Show actual parameter values used in testing
- Include HTTP method for API method understanding
- Keep format consistent across all endpoint tests

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
- **Breaking Changes**: v2.0+ includes buylist endpoints restoration
- **Python Support**: 3.8-3.12
- **License**: MIT

---


### Current Status: **Priority 1 Parameter Fixes Complete - Testing Infrastructure Updated** ✅

**Latest Testing Results (September 8, 2025)**: All Priority 1 fixes validated and working

#### **✅ Completed Priority 1 Achievements**
- **Rate Limiter Logic Fixed**: Corrected bug where rates under 10 req/sec were being forced to 10
- **Comprehensive .env Configuration**: Added 22+ config variables with detailed comments
- **Playwright Documentation Verification**: Systematically validated API documentation for error endpoints
- **Priority 1 Parameter Fixes**: All 3 critical parameter fixes completed and validated ✅

#### **🎯 Priority 1 Parameter Fixes - COMPLETED ✅**
1. **"Get Store Buylist Products for Kiosk"** ✅ - Added all 5 optional query parameters:
   - `searchTerm` (string, optional)
   - `offset` (int32, optional) 
   - `limit` (int32, optional)
   - `sortDirection` (string, optional)
   - `categoryId` (int32, optional)

2. **"Search Custom Listings"** ✅ - Added required query parameter:
   - `photoId` (int32, required)

3. **"Get Product Conditions for Store Buylist"** ✅ - Fixed URL structure:
   - Fixed: `/stores/{storeKey}/buylist/{productId}`

#### **📊 Current Endpoint Status (Verified with Correct Method Names)**
- **App Endpoints**: 1/1 working (100%) ✅
- **Catalog Endpoints**: 21/21 working (100%) ✅ 
- **Inventory Endpoints**: 0/4 working (0%) - Expected due to permissions
- **Pricing Endpoints**: 7/7 working (100%) ✅
- **Store Priority 1 Fixes**: 3/3 working (100%) ✅

#### **🔧 Testing Infrastructure Fixes**
- **Method Name Regression Fixed**: Corrected test method names that caused false failures
- **Test Data Updated**: Using valid GTINs (889698355100) and product IDs (152944)
- **Comprehensive Testing**: Must test ALL 80 endpoints every time, no shortcuts

**🔴 Priority 2: POST Method Issues**
- [ ] **List Product Summary By Category** - Currently GET, should be POST with request body
- [ ] **Search Top Sold Products** - Currently GET, should be POST with request body

**🟡 Priority 3: Additional Parameter Verification**
- [ ] **Get Buylist Categories** - Check for missing query parameters
- [ ] **Get Buylist Groups** - Check for missing query parameters
- [ ] **Get Store Buylist Settings** - Check for missing query parameters
- [ ] **Get Store Info by Key** - Verify parameter format requirements
- [ ] **Get SKU List Price** - Verify parameter requirements

**🎯 Target**: Achieve 70%+ endpoint success rate (56/80 endpoints)

---

## 📖 Ref MCP Usage Guidelines

**IMPORTANT**: When using the Ref MCP tool, follow these specific guidelines:

### ✅ USE Ref FOR:
- **Python syntax and language features** (async/await, type hints, decorators, etc.)
- **Testing methodology** (pytest patterns, mocking, fixtures, parametrization)
- **Dependency documentation** (aiohttp, pydantic, mypy usage patterns)  
- **General coding practices** (error handling, design patterns, best practices)
- **Code quality tools** (black, flake8, mypy configuration and usage)

### ❌ DO NOT USE Ref FOR:
- **TCGplayer API specifics** - Use local `api-endpoints.json` as single source of truth
- **Project-specific endpoints** - All endpoint specs are in local documentation
- **TCGplayer business logic** - Rely on existing codebase patterns and local files

### Usage Pattern:
```bash
# ✅ Good: Research Python/testing patterns before implementation
mcp__Ref__ref_search_documentation("python async context manager pytest fixtures")

# ❌ Bad: Research TCGplayer API details  
mcp__Ref__ref_search_documentation("TCGplayer store endpoints storeKey")
```

This ensures we use authoritative local API documentation while leveraging Ref for general programming knowledge.