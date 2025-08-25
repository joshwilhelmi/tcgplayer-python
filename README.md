# TCGplayer Client - Python API Client

[![Python
3.8+](<https://img.shields.io/badge/python-3.8+-blue.svg)>](<https://www.python.org/downloads/)>
[![License:
MIT](<https://img.shields.io/badge/License-MIT-yellow.svg)>](<https://opensource.org/licenses/MIT)>
[![Code style:
black](<https://img.shields.io/badge/code%20style-black-000000.svg)>](<https://github.com/psf/black)>
[![Imports:
isort](<https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)>](<https://pycqa.github.io/isort/)>

## ⚠️ **CRITICAL RATE LIMITING WARNING**

**TCGplayer's API enforces a hard maximum of 10 requests per second.** Exceeding
this limit can result in:

- API access being permanently revoked
- Account suspension
- Legal consequences

This client automatically enforces this limit to protect your API access.

A comprehensive, production-ready Python client library for the TCGplayer API
with async support, intelligent rate limiting, caching, and comprehensive
endpoint coverage. Built for developers who need reliable, scalable access to
TCGplayer's trading card data.

## 🚀 Features

- **🔌 Full API Coverage**: All 55+ documented TCGplayer API endpoints with
comprehensive error handling (buylist endpoints removed - discontinued by
TCGPlayer)
- **⚡ Async/Await Support**: Built with modern Python async patterns for
high-performance applications
- **🔄 Intelligent Rate Limiting**: Adaptive request throttling that respects API
limits and prevents rate limit errors
- **💾 Smart Caching**: Configurable response caching with TTL and LRU eviction
for improved performance
- **🔐 Robust Authentication**: OAuth2 token management with automatic refresh
and session persistence
- **🛡️ Enterprise-Grade Error Handling**: Custom exception hierarchy with
detailed error context and retry logic
- **📊 Comprehensive Logging**: Structured logging with configurable levels and
multiple output formats
- **⚙️ Flexible Configuration**: Environment variables, config files, and
runtime configuration management
- **🧪 Full Test Coverage**: Comprehensive test suite with pytest and async
testing support
- **📝 Type Hints**: Full type annotation support for better development
experience and IDE integration

## 📦 Installation

### From Source (Development)

```bash

git clone <https://github.com/joshwilhelmi/tcgplayer-python.git>
cd tcgplayer-python
pip install -e .

```

### From PyPI

```bash

pip install tcgplayer-client

```

## 🚀 Quick Start

### Migration from v1.x

If you're upgrading from version 1.x, be aware of these breaking changes:

```python

# ❌ OLD (v1.x) - Buylist methods (no longer available)


# await client.endpoints.buylist.get_buylist_prices([12345])


# await client.endpoints.pricing.get_buylist_prices([12345])

# ✅ NEW (v2.0.1) - Market prices only

await client.endpoints.pricing.get_market_prices([12345])
await client.endpoints.pricing.get_sku_market_prices([67890])

```

**Note**: Buylist functionality was discontinued by TCGPlayer and has been
removed from this client.

### Basic Usage

```python

import asyncio
from tcgplayer_client import TCGPlayerClient

async def main():
    # Initialize client with your API credentials
    client = TCGPlayerClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )
    
    # Authenticate automatically
    await client.authenticate()
    
    # Use endpoints
    categories = await client.endpoints.catalog.get_categories()
    print(f"Found {len(categories)} product categories")
    
    # Get pricing for a specific product
    prices = await client.endpoints.pricing.get_product_prices(product_id=12345)
    print(f"Product prices: {prices}")

if __name__ == "__main__":
    asyncio.run(main())

```

### Advanced Configuration

```python

from tcgplayer_client import TCGPlayerClient, ClientConfig

# Custom configuration

config = ClientConfig(
    max_requests_per_second=20,
    enable_caching=True,
    cache_ttl=300,  # 5 minutes
    log_level="DEBUG"
)

client = TCGPlayerClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    config=config
)

```

### Environment Variables

```bash

export TCGPLAYER_CLIENT_ID="your_client_id"
export TCGPLAYER_CLIENT_SECRET="your_client_secret"
export TCGPLAYER_LOG_LEVEL="INFO"
export TCGPLAYER_ENABLE_CACHING="true"
export TCGPLAYER_CACHE_TTL="300"

```

## 🔌 API Endpoints

The client provides organized access to all TCGplayer API endpoints through
specialized endpoint classes:

### 📚 Catalog Endpoints

- **Categories**: Product categories and hierarchies
- **Groups**: Product groups and classifications  
- **Products**: Detailed product information
- **Search**: Advanced product search and filtering

### 💰 Pricing Endpoints

- **Market Prices**: Current market pricing data
- **Price Guides**: Historical price trends and guides
- **SKU Pricing**: Product variant pricing information

### 🏪 Store Endpoints

- **Store Information**: Store details and metadata
- **Store Inventory**: Available inventory and stock levels
- **Store Locations**: Geographic store information

### 📦 Order Endpoints

- **Order Management**: Create, update, and track orders
- **Order History**: Historical order data and analytics
- **Order Status**: Real-time order status updates

### 📋 Inventory Endpoints

- **Inventory Management**: Add, update, and remove inventory
- **Stock Levels**: Current stock quantities and availability
- **Inventory Analytics**: Inventory performance metrics

## ⚙️ Configuration

### ⚠️ **Critical Rate Limiting Restriction**

**IMPORTANT**: TCGplayer's API enforces a **hard maximum of 10 requests per
second**. Exceeding this limit can result in:

- API access being temporarily suspended
- Permanent API access revocation
- Account restrictions

The client **automatically enforces this limit** regardless of your
configuration to prevent API violations.

### Client Configuration

```python

from tcgplayer_client import ClientConfig

config = ClientConfig(
    # API Configuration
    base_url="<https://api.tcgplayer.com>",
    api_version="v1.0",
    
    # Rate Limiting (MAXIMUM: 10 requests per second)
    max_requests_per_second=10,  # Will be capped to 10 if higher
    rate_limit_window=1.0,
    max_retries=3,
    base_delay=1.0,
    
    # Session Management
    max_connections=100,
    max_connections_per_host=10,
    keepalive_timeout=30.0,
    
    # Caching
    enable_caching=True,
    cache_ttl=300,
    max_cache_size=1000,
    
    # Logging
    log_level="INFO",
    log_file="tcgplayer.log",
    enable_console_logging=True,
    enable_file_logging=True
)

```

### Rate Limiting

```python

client = TCGPlayerClient(
    max_requests_per_second=20,    # ⚠️ Will be automatically capped to 10
    rate_limit_window=1.0,         # 1 second window
    max_retries=5,                 # 5 retry attempts
    base_delay=2.0                 # 2 second base delay
)

# The client will log a warning and cap the rate limit to 10 req/s


# This prevents accidental API violations

```

### Caching Configuration

```python

client = TCGPlayerClient(
    config=ClientConfig(
        enable_caching=True,
        cache_ttl=600,              # 10 minutes
        max_cache_size=5000,        # 5000 cached responses
        cache_cleanup_interval=300  # Cleanup every 5 minutes
    )
)

```

## 🛡️ Error Handling

The library provides a comprehensive exception hierarchy for different error
scenarios:

```python

from tcgplayer_client import (
    TCGPlayerError,
    AuthenticationError,
    RateLimitError,
    APIError,
    NetworkError,
    TimeoutError,
    RetryExhaustedError,
    InvalidResponseError
)

try:
    result = await client.endpoints.catalog.get_categories()
except AuthenticationError:
    print("Authentication failed - check your credentials")
except RateLimitError as e:
    print(f"Rate limit exceeded - retry after {e.retry_after} seconds")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
    print(f"Error type: {e.error_type}")
    print(f"Request ID: {e.request_id}")
except NetworkError as e:
    print(f"Network error: {e}")
    print(f"Retry count: {e.retry_count}")
except TimeoutError:
    print("Request timed out")
except RetryExhaustedError:
    print("Max retries exceeded")

```

### Error Context and Retry Information

```python

try:
    result = await client.endpoints.pricing.get_product_prices(product_id=12345)
except APIError as e:
    print(f"Error occurred during pricing request:")
    print(f"  Endpoint: {e.endpoint}")
    print(f"  Method: {e.method}")
    print(f"  Status: {e.status_code}")
    print(f"  Message: {e.message}")
    print(f"  Request ID: {e.request_id}")
    print(f"  Timestamp: {e.timestamp}")

```

## 📊 Logging

### Basic Logging Setup

```python

from tcgplayer_client.logging_config import setup_logging, get_logger

# Setup logging with default configuration

setup_logging()

# Get logger for your module

logger = get_logger(__name__)

# Use structured logging

logger.info("Starting TCGplayer client", extra={
    "client_id": "your_client_id",
    "endpoint": "catalog",
    "operation": "get_categories"
})

```

### Advanced Logging Configuration

```python

from tcgplayer_client.logging_config import TCGPlayerLogger

# Custom logger configuration

logger = TCGPlayerLogger(
    name="my_app",
    level="DEBUG",
    enable_console=True,
    enable_file=True,
    log_file="app.log",
    enable_json=True,
    formatter="structured"
)

logger.info("Custom logger configured", extra={"component": "tcgplayer_client"})

```

## 🔧 Development

### Setup Development Environment

```bash

# Clone repository

git clone <https://github.com/joshwilhelmi/tcgplayer-python.git>
cd tcgplayer-python

# Create virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode

pip install -e ".[dev]"

# Install pre-commit hooks (optional)

pre-commit install

```

### Local Testing Pipeline

The project includes a comprehensive local testing pipeline that mimics GitHub
Actions:

```bash

# Run full local CI pipeline (recommended before pushing)

make ci

# Quick quality checks

make quick-check

# Individual tools

make format      # Black + isort
make lint        # Flake8
make type-check  # MyPy
make security    # Bandit + Safety + Semgrep
make test        # Pytest with coverage

# See [LOCAL_TESTING.md](LOCAL_TESTING.md) for detailed usage
```

### Running Tests

```bash

# Run all tests

pytest

# Run with coverage

pytest --cov=tcgplayer_client --cov-report=html

# Run specific test file

pytest tests/test_client.py

# Run tests with verbose output

pytest -v

# Run tests in parallel

pytest -n auto

```

### Code Quality

```bash

# Code formatting

black .
isort .

# Linting

flake8 tcgplayer_client/
mypy tcgplayer_client/

# Run all quality checks

make quality  # If Makefile is available

```

### Security Testing

```bash

# Security scanning with Bandit

bandit -r tcgplayer_client/ -f json -o bandit-report.json

# Dependency vulnerability scanning

safety check

# Advanced security analysis

pip install semgrep
semgrep --config=auto tcgplayer_client/

# Dependency security audit

pip-audit

```

**Note**: Security issues have been identified and fixed in the codebase:

- ✅ **MD5 → SHA256**: Replaced weak MD5 hashing with secure SHA256 for cache
keys
- ✅ **Try-except-pass**: Fixed silent exception handling with proper logging
- ✅ **Assert statements**: Replaced with proper runtime error handling

**✅ COMPLETED**: Security tools are now integrated into the CI/CD pipeline for
automated security testing.

### **Comprehensive Testing Strategy**

The project includes multiple layers of testing to ensure code quality and
security:

#### **1. Unit Testing (pytest)**

```bash

# Run all tests with coverage

pytest --cov=tcgplayer_client --cov-report=html --cov-report=term-missing

# Run specific test categories

pytest tests/test_auth.py          # Authentication tests
pytest tests/test_client.py        # Main client tests
pytest tests/test_endpoints/       # API endpoint tests
pytest tests/test_rate_limiter.py  # Rate limiting tests
pytest tests/test_cache.py         # Caching tests

# Run tests in parallel

pytest -n auto --dist=loadfile

# Generate coverage reports

pytest --cov=tcgplayer_client --cov-report=html --cov-report=xml

```

#### **2. Security Testing (Automated)**

```bash

# Bandit security scanning

bandit -r tcgplayer_client/ -f json -o bandit-report.json
bandit -r tcgplayer_client/ -f txt

# Safety dependency scanning

safety check --json --output safety-report.json
safety check

# Semgrep static analysis

semgrep --config=auto --json --output=semgrep-report.json tcgplayer_client/

# Pip audit for dependencies

pip-audit --desc --format=json --output=pip-audit-report.json

```

#### **3. Code Quality Testing**

```bash

# Black code formatting

black --check --diff .

# Import sorting

isort --check-only --diff .

# Flake8 linting

flake8 tcgplayer_client/ tests/ --max-line-length=88 --extend-ignore=E203,W503

# MyPy type checking

mypy tcgplayer_client/ --ignore-missing-imports

# Pre-commit hooks (if installed)

pre-commit run --all-files

```

#### **4. Performance Testing**

```bash

# Run performance benchmarks

python -m pytest tests/test_performance.py -v

# Memory usage profiling

python -m memory_profiler tests/test_memory.py

# Async performance testing

python -m pytest tests/test_async_performance.py -v

```

#### **5. Integration Testing**

```bash

# Test with real TCGplayer API (requires credentials)

export TCGPLAYER_CLIENT_ID="your_client_id"
export TCGPLAYER_CLIENT_SECRET="your_client_secret"
python -m pytest tests/test_integration.py -v

# Test rate limiting compliance

python -m pytest tests/test_rate_limit_compliance.py -v

```

#### **6. Test Coverage Goals**

- **Current Coverage**: 95%+ (90+ tests passing)
- **Target Coverage**: 95%+ for production quality
- **Critical Paths**: 100% coverage for authentication, rate limiting, and error
handling
- **New Features**: 95%+ coverage requirement before merge

### Testing Examples

```python

import pytest
from tcgplayer_client import TCGPlayerClient

@pytest.mark.asyncio
async def test_catalog_endpoints():
    client = TCGPlayerClient()
    
    # Test categories endpoint
    categories = await client.endpoints.catalog.get_categories()
    assert isinstance(categories, list)
    assert len(categories) > 0
    
    # Test product search
    products = await client.endpoints.catalog.search_products(
        search_term="Black Lotus"
    )
    assert isinstance(products, list)

```

## 📋 Requirements

### Core Dependencies

- **Python**: 3.8 or higher
- **aiohttp**: 3.8.0 or higher (async HTTP client)

### Development Dependencies

- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

## 🏗️ Architecture

### Core Components

```text
tcgplayer_client/
├── client.py              # Main client class
├── auth.py                # Authentication management
├── rate_limiter.py        # Rate limiting and throttling
├── session_manager.py     # HTTP session management
├── cache.py               # Response caching system
├── config.py              # Configuration management
├── validation.py          # Input validation
├── logging_config.py      # Logging configuration
├── exceptions.py          # Custom exception hierarchy
└── endpoints/             # API endpoint implementations
    ├── catalog.py         # Catalog operations
    ├── pricing.py         # Pricing operations
    ├── stores.py          # Store operations
    ├── orders.py          # Order operations
    ├── inventory.py       # Inventory operations
    └── pricing.py         # Pricing operations (market prices, price guides)
```

### Design Patterns

- **Async/Await**: Modern Python async patterns for non-blocking I/O
- **Factory Pattern**: Endpoint creation and management
- **Strategy Pattern**: Configurable rate limiting and caching strategies
- **Observer Pattern**: Event-driven logging and monitoring
- **Builder Pattern**: Configuration object construction

## 📚 Examples

### Bulk Product Processing

```python

async def process_products_bulk(client, product_ids):
    """Process multiple products efficiently with rate limiting."""
    results = []
    
    for product_id in product_ids:
        try:
            # Get product details
            product = await client.endpoints.catalog.get_product(product_id)
            
            # Get current pricing
pricing = await client.endpoints.pricing.get_product_prices(product_id)
            
            # Get store inventory
inventory = await client.endpoints.stores.get_store_inventory(product_id)
            
            results.append({
                'product': product,
                'pricing': pricing,
                'inventory': inventory
            })
            
        except Exception as e:
            logger.error(f"Error processing product {product_id}: {e}")
            continue
    
    return results

```

### Store Inventory Monitoring

```python

async def monitor_store_inventory(client, store_id, product_ids):
    """Monitor store inventory levels for specific products."""
    while True:
        try:
            for product_id in product_ids:
                inventory = await client.endpoints.stores.get_store_inventory(
                    store_id=store_id,
                    product_id=product_id
                )
                
                if inventory and inventory.get('quantity', 0) > 0:
logger.info(f"Product {product_id} available at store {store_id}")
                    
            # Wait before next check
            await asyncio.sleep(300)  # 5 minutes
            
        except Exception as e:
            logger.error(f"Inventory monitoring error: {e}")
            await asyncio.sleep(60)  # Wait 1 minute on error

```

### Price Alert System

```python

async def price_alert_system(client, product_id, target_price):
    """Monitor product prices and alert when target price is reached."""
    while True:
        try:
prices = await client.endpoints.pricing.get_product_prices(product_id)
            
            if prices and len(prices) > 0:
                current_price = prices[0].get('price', float('inf'))
                
                if current_price <= target_price:
logger.info(f"Price alert! Product {product_id} is now ${current_price}")
                    # Send notification (email, webhook, etc.)
                    break
            
            await asyncio.sleep(3600)  # Check every hour
            
        except Exception as e:
            logger.error(f"Price monitoring error: {e}")
            await asyncio.sleep(300)  # Wait 5 minutes on error

```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing
Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write comprehensive docstrings
- Include tests for new functionality
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

## 🆘 Support

### Getting Help

- **📖 Documentation**: This README and inline code documentation
- **🐛 Issues**: [GitHub
Issues](<https://github.com/joshwilhelmi/tcgplayer-python/issues)>
- **💬 Discussions**: [GitHub
Discussions](<https://github.com/joshwilhelmi/tcgplayer-python/discussions)>
- **📧 Email**: [josh@gobby.ai](mailto:josh@gobby.ai)

### Common Issues

#### Authentication Errors

- Verify your `client_id` and `client_secret` are correct
- Check that your TCGplayer API account is active
- Ensure your IP address is whitelisted if required

#### Rate Limiting Issues

- Reduce your request frequency
- Implement exponential backoff in your application
- Use the built-in rate limiting features

#### Network Issues

- Check your internet connection
- Verify firewall settings
- Use the retry mechanisms built into the client

## 📈 Roadmap

### Upcoming Features

- [ ] **WebSocket Support**: Real-time data streaming
- [ ] **GraphQL Interface**: Alternative to REST API
- [ ] **Data Export**: CSV/JSON export functionality
- [ ] **Analytics Dashboard**: Built-in data visualization
- [ ] **Webhook Support**: Event-driven notifications
- [ ] **Multi-API Support**: Integration with other trading card APIs

### Version History

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes and
improvements.

## 🙏 Acknowledgments

- **TCGplayer** for providing the comprehensive API
- **Python Community** for excellent async libraries and tools
- **Contributors** who help improve this library
- **Open Source Community** for inspiration and best practices

## 📊 Project Status

- **Development Status**: Production Ready
- **Python Version Support**: 3.8+
- **Test Coverage**: 95%+
- **Documentation**: Comprehensive
- **License**: MIT (Open Source)
- **CI/CD**: Automated testing, security scanning, and PyPI publishing

---

**Made with ❤️ by [Josh Wilhelmi](mailto:josh@gobby.ai)**

*If you find this library helpful, please consider giving it a ⭐ on GitHub!*
