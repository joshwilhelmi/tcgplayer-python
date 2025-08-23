# TCGPlayer Client

A comprehensive Python client library for the TCGPlayer API with async support, rate limiting, and comprehensive endpoint coverage.

## Features

- **Full API Coverage**: All 67 documented TCGPlayer API endpoints
- **Async/Await Support**: Built with modern Python async patterns
- **Rate Limiting**: Intelligent request throttling to respect API limits
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Authentication**: OAuth2 token management with automatic refresh
- **Type Hints**: Full type annotation support for better development experience

## Installation

### From Source (Development)

```bash
git clone https://github.com/joshwilhelmi/tcgplayer-python.git
cd tcgplayer-python
pip install -e .
```

### From PyPI (Future)

```bash
pip install tcgplayer-client
```

## Quick Start

```python
import asyncio
from tcgplayer_client import TCGPlayerClient

async def main():
    # Initialize client with your API credentials
    client = TCGPlayerClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )
    
    # Authenticate
    await client.authenticate()
    
    # Use endpoints
    catalog = await client.endpoints.catalog.get_categories()
    print(f"Found {len(catalog)} categories")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Endpoints

The client provides access to all TCGPlayer API endpoints through organized endpoint classes:

- **Catalog**: Product categories, groups, and details
- **Pricing**: Market prices and price guides
- **Stores**: Store information and inventory
- **Orders**: Order management and tracking
- **Inventory**: Inventory management
- **Buylist**: Buylist operations

## Configuration

### Rate Limiting

```python
client = TCGPlayerClient(
    max_requests_per_second=10,  # Default: 10
    rate_limit_window=1.0,       # Default: 1.0 seconds
    max_retries=3,               # Default: 3
    base_delay=1.0               # Default: 1.0 seconds
)
```

### Authentication

```python
# Environment variables
export TCGPLAYER_CLIENT_ID="your_client_id"
export TCGPLAYER_CLIENT_SECRET="your_client_secret"

# Or pass directly
client = TCGPlayerClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
```

## Error Handling

The library provides specific exception types for different error scenarios:

```python
from tcgplayer_client import (
    TCGPlayerError,
    AuthenticationError,
    RateLimitError,
    APIError,
    NetworkError
)

try:
    result = await client.endpoints.catalog.get_categories()
except AuthenticationError:
    print("Authentication failed")
except RateLimitError:
    print("Rate limit exceeded")
except APIError as e:
    print(f"API error: {e}")
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
black .
isort .

# Linting
flake8
mypy .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tcgplayer_client --cov-report=html

# Run specific test file
pytest tests/test_client.py
```

## Requirements

- Python 3.8+
- aiohttp 3.8.0+

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/joshwilhelmi/tcgplayer-python/issues)
- **Documentation**: [API Reference](https://github.com/joshwilhelmi/tcgplayer-python#readme)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Author

**Josh Wilhelmi** - [josh@gobby.ai](mailto:josh@gobby.ai)

## Acknowledgments

- TCGPlayer for providing the API
- The Python community for excellent async libraries
