"""
TCGPlayer Client Library

A Python client library for the TCGPlayer API with support for:
- Authentication and rate limiting
- All 67 documented API endpoints
- Async/await support
- Comprehensive error handling
"""

from .auth import TCGPlayerAuth
from .cache import (
    CacheEntry,
    CacheKeyGenerator,
    CacheManager,
    LRUCache,
    ResponseCache,
)
from .client import TCGPlayerClient
from .config import (
    ClientConfig,
    ConfigurationManager,
    create_default_config,
    get_env_bool,
    get_env_float,
    get_env_int,
    load_config,
)
from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    InvalidResponseError,
    NetworkError,
    RateLimitError,
    RetryExhaustedError,
    TCGPlayerError,
    TimeoutError,
    ValidationError,
)
from .logging_config import (
    StructuredFormatter,
    TCGPlayerLogger,
    get_logger,
    setup_logging,
)
from .rate_limiter import RateLimiter
from .validation import (
    ParameterValidator,
    validate_id,
    validate_non_negative_integer,
    validate_positive_float,
    validate_positive_integer,
)

__version__ = "2.0.3"
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
