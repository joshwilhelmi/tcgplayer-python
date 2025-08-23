"""
TCGPlayer Client Library

A Python client library for the TCGPlayer API with support for:
- Authentication and rate limiting
- All 67 documented API endpoints
- Async/await support
- Comprehensive error handling
"""

from .auth import TCGPlayerAuth
from .client import TCGPlayerClient
from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    NetworkError,
    RateLimitError,
    TCGPlayerError,
    ValidationError,
    TimeoutError,
    RetryExhaustedError,
    InvalidResponseError,
)
from .rate_limiter import RateLimiter
from .validation import (
    ParameterValidator,
    validate_id,
    validate_positive_integer,
    validate_non_negative_integer,
    validate_positive_float,
)
from .logging_config import (
    TCGPlayerLogger,
    setup_logging,
    get_logger,
    StructuredFormatter,
)
from .config import (
    ClientConfig,
    ConfigurationManager,
    load_config,
    create_default_config,
    get_env_bool,
    get_env_int,
    get_env_float,
)
from .cache import (
    ResponseCache,
    CacheManager,
    LRUCache,
    CacheEntry,
    CacheKeyGenerator,
)

__version__ = "1.0.0"
__author__ = "Josh Wilhelmi"
__description__ = "Python client library for TCGPlayer API"

__all__ = [
    "TCGPlayerClient",
    "TCGPlayerAuth",
    "RateLimiter",
    "ParameterValidator",
    "validate_id",
    "validate_positive_integer",
    "validate_non_negative_integer",
    "validate_positive_float",
    "TCGPlayerLogger",
    "setup_logging",
    "get_logger",
    "StructuredFormatter",
    "ClientConfig",
    "ConfigurationManager",
    "load_config",
    "create_default_config",
    "get_env_bool",
    "get_env_int",
    "get_env_float",
    "ResponseCache",
    "CacheManager",
    "LRUCache",
    "CacheEntry",
    "CacheKeyGenerator",
    "TCGPlayerError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    "NetworkError",
    "ValidationError",
    "ConfigurationError",
    "TimeoutError",
    "RetryExhaustedError",
    "InvalidResponseError",
]
