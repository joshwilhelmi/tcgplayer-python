"""
Main TCGPlayer client class for API interactions.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

import aiohttp

from .auth import TCGPlayerAuth
from .cache import CacheManager, ResponseCache
from .config import ClientConfig, load_config
from .exceptions import (
    APIError,
    AuthenticationError,
    InvalidResponseError,
    NetworkError,
    RateLimitError,
    RetryExhaustedError,
    TimeoutError,
)
from .rate_limiter import RateLimiter
from .session_manager import SessionManager

logger = logging.getLogger(__name__)


class TCGPlayerClient:
    """Main client for interacting with the TCGPlayer API."""

    # Type annotations for instance attributes
    cache_manager: Optional[CacheManager]
    response_cache: Optional[ResponseCache]

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        max_requests_per_second: int = 10,
        rate_limit_window: float = 1.0,
        max_retries: int = 3,
        base_delay: float = 1.0,
        config: Optional[ClientConfig] = None,
    ) -> None:
        """
        Initialize the TCGPlayer client.

        Args:
            client_id: TCGPlayer API client ID
            client_secret: TCGPlayer API client secret
            max_requests_per_second: Maximum requests per second (default: 10, max: 10)
            rate_limit_window: Rate limit window in seconds (default: 1.0)
            max_retries: Maximum retry attempts for failed requests (default: 3)
            base_delay: Base delay for retry backoff in seconds (default: 1.0)
            config: Optional configuration object

        Note:
            The maximum rate limit is capped at 10 requests per second to comply with
            TCGPlayer's API restrictions. Exceeding this limit can result in API access
            being revoked.
        """
        # Validate rate limiting parameters
        if max_requests_per_second > 10:
            logger.warning(
                f"Requested rate limit {max_requests_per_second} req/s exceeds "
                f"TCGPlayer's maximum of 10 req/s. Rate limit has been capped to "
                f"10 req/s to prevent API violations."
            )
            max_requests_per_second = 10

        # Load configuration
        if config is None:
            try:
                config = load_config()
            except Exception:
                # Use defaults if config loading fails
                config = ClientConfig()

        self.config = config

        # Initialize authentication (optional for testing)
        self.auth: Optional[TCGPlayerAuth] = (
            TCGPlayerAuth(
                client_id or config.client_id,
                client_secret or config.client_secret,
                base_url=config.base_url,
            )
            if (client_id or config.client_id)
            and (client_secret or config.client_secret)
            else None
        )

        # API configuration
        self.base_url: str = config.base_url

        # Session management with configuration
        self.session_manager: SessionManager = SessionManager(
            max_connections=config.max_connections,
            max_connections_per_host=config.max_connections_per_host,
            keepalive_timeout=config.keepalive_timeout,
        )

        # Rate limiting configuration (prioritize passed parameters, but enforce
        # maximum)
        config_rate_limit = config.max_requests_per_second or 10
        if config_rate_limit > 10:
            logger.warning(
                f"Configuration rate limit {config_rate_limit} req/s exceeds "
                f"TCGPlayer's maximum. "
                f"Capping to 10 req/s to prevent API violations."
            )
            config_rate_limit = 10

        self.rate_limiter: RateLimiter = RateLimiter(
            max_requests_per_second or config_rate_limit,
            rate_limit_window or config.rate_limit_window,
        )

        # Request retry configuration (prioritize passed parameters)
        self.max_retries: int = max_retries or config.max_retries
        self.base_delay: float = base_delay or config.base_delay

        # Caching configuration
        if config.enable_caching:
            self.cache_manager = CacheManager(
                {
                    "default": {
                        "max_size": config.cache_max_size,
                        "default_ttl": config.cache_ttl,
                        "enable_compression": False,
                    }
                }
            )
            self.response_cache = self.cache_manager.get_default_cache()
        else:
            self.cache_manager = None
            self.response_cache = None

        # Initialize endpoint classes
        from .endpoints import (
            CatalogEndpoints,
            InventoryEndpoints,
            OrderEndpoints,
            PricingEndpoints,
            StoreEndpoints,
        )

        self.endpoints = type(
            "Endpoints",
            (),
            {
                "catalog": CatalogEndpoints(self),
                "pricing": PricingEndpoints(self),
                "stores": StoreEndpoints(self),
                "orders": OrderEndpoints(self),
                "inventory": InventoryEndpoints(self),
            },
        )()

        logger.info(
            f"TCGPlayer client initialized with rate limit: "
            f"{max_requests_per_second} req/s (TCGPlayer maximum: 10 req/s)"
        )
        logger.info(
            f"Retry configuration: max {max_retries} attempts, base delay {base_delay}s"
        )
        logger.info("All endpoint modules loaded successfully")

    async def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate with the TCGPlayer API.

        Returns:
            Authentication result

        Raises:
            AuthenticationError: If authentication fails
        """
        if not self.auth:
            raise AuthenticationError(
                "No authentication configured. Provide client_id and client_secret."
            )
        return await self.auth.authenticate()

    async def _make_api_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        use_cache: bool = True,
        cache_ttl: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Make an authenticated API request to TCGPlayer with rate limiting and retry
        logic.

        Args:
            endpoint: API endpoint path
            params: Query parameters
            method: HTTP method (GET, POST, PUT)
            data: Request body data for POST/PUT requests (dict or list of dicts)
            use_cache: Whether to use caching for GET requests
            cache_ttl: Custom TTL for cached responses

        Returns:
            API response data

        Raises:
            AuthenticationError: If not authenticated
            RateLimitError: If rate limit is exceeded
            APIError: If API returns an error
            NetworkError: If network error occurs
        """
        if not self.auth:
            raise AuthenticationError(
                "No authentication configured. Provide client_id and client_secret."
            )
        if not self.auth.is_authenticated():
            raise AuthenticationError("Not authenticated. Call authenticate() first.")

        # Check cache for GET requests
        if use_cache and method == "GET" and self.response_cache:
            cached_response = await self.response_cache.get_cached_response(
                endpoint, params, method, data
            )
            if cached_response is not None:
                logger.info(f"Cache hit for {endpoint}")
                return cached_response

        headers = {
            "Authorization": f"Bearer {self.auth.get_access_token()}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}{endpoint}"
        if params:
            url += f"?{urlencode(params)}"

        for attempt in range(self.max_retries):
            try:
                # Acquire rate limit permission
                await self.rate_limiter.acquire()

                logger.info(
                    f"Making {method} API request to {endpoint} "
                    f"(attempt {attempt + 1}/{self.max_retries})"
                )

                async with self.session_manager.session_context() as session:
                    if method == "POST":
                        async with session.post(
                            url, headers=headers, json=data
                        ) as response:
                            return await self._handle_response(
                                response,
                                endpoint,
                                use_cache,
                                method,
                                params,
                                data,
                                cache_ttl,
                            )
                    elif method == "PUT":
                        async with session.put(
                            url, headers=headers, json=data
                        ) as response:
                            return await self._handle_response(
                                response,
                                endpoint,
                                use_cache,
                                method,
                                params,
                                data,
                                cache_ttl,
                            )
                    else:
                        async with session.get(url, headers=headers) as response:
                            return await self._handle_response(
                                response,
                                endpoint,
                                use_cache,
                                method,
                                params,
                                data,
                                cache_ttl,
                            )

            except asyncio.TimeoutError:
                if attempt < self.max_retries - 1:
                    wait_time = self.base_delay * (2**attempt)
                    logger.warning(
                        f"Request timeout. Retrying in {wait_time} seconds..."
                    )
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise TimeoutError(
                        f"API request timed out after {self.max_retries} attempts",
                        timeout_seconds=(
                            self.timeout.total if hasattr(self, "timeout") else None
                        ),
                    )

            except aiohttp.ClientError as e:
                if attempt < self.max_retries - 1:
                    wait_time = self.base_delay * (2**attempt)
                    logger.warning(
                        f"Network error: {e}. Retrying in {wait_time} seconds..."
                    )
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise NetworkError(
                        f"Network error after {self.max_retries} attempts: {e}"
                    )

        raise RetryExhaustedError(
            f"API request failed after {self.max_retries} attempts",
            attempts_made=self.max_retries,
            last_error=None,
        )

    async def _handle_response(
        self,
        response: aiohttp.ClientResponse,
        endpoint: str,
        use_cache: bool = True,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        cache_ttl: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Handle API response and extract data or raise appropriate exceptions.

        Args:
            response: HTTP response object
            endpoint: API endpoint for logging
            use_cache: Whether to cache successful responses
            method: HTTP method used
            params: Query parameters used
            data: Request body data used
            cache_ttl: Custom TTL for cached responses

        Returns:
            Response data

        Raises:
            RateLimitError: If rate limit exceeded
            APIError: If API returns error status
        """
        if response.status == 200:
            try:
                result = await response.json()
                logger.info(f"API request successful: {endpoint}")

                # Cache successful GET responses
                if use_cache and method == "GET" and self.response_cache:
                    await self.response_cache.cache_response(
                        endpoint, params, method, data, result, 200, cache_ttl
                    )

                return result
            except Exception as e:
                logger.error(f"Failed to parse JSON response from {endpoint}: {e}")
                raise InvalidResponseError(
                    f"Invalid JSON response from {endpoint}",
                    response_data=await response.text(),
                )
        elif response.status == 429:  # Too Many Requests
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                wait_time = int(retry_after)
                raise RateLimitError(
                    f"Rate limit exceeded. Retry after {wait_time} seconds.", wait_time
                )
            else:
                raise RateLimitError("Rate limit exceeded.")
        elif response.status in (500, 502, 503, 504):  # Server errors
            error_text = await response.text()
            raise APIError(
                f"Server error {response.status}: {error_text}",
                response.status,
                error_text,
            )
        else:
            error_text = await response.text()
            raise APIError(
                f"API request failed: {response.status} - {error_text}",
                response.status,
                error_text,
            )

    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Get current rate limit status.

        Returns:
            Rate limiter status information
        """
        return self.rate_limiter.get_status()

    async def get_rate_limit_status_async(self) -> Dict[str, Any]:
        """
        Get current rate limit status asynchronously.

        Returns:
            Rate limiter status information
        """
        return await self.rate_limiter.get_status_async()

    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        if not self.auth:
            return False
        return self.auth.is_authenticated()

    async def close(self) -> None:
        """Close the client and cleanup resources."""
        await self.session_manager.cleanup()
        if self.cache_manager:
            await self.cache_manager.close_all()
        logger.info("TCGPlayer client closed and resources cleaned up")

    async def clear_cache(self) -> None:
        """Clear all cached responses."""
        if self.response_cache:
            await self.response_cache.clear()
            logger.info("Response cache cleared")

    async def get_cache_stats(self) -> Optional[Dict[str, Any]]:
        """Get cache statistics if caching is enabled."""
        if self.response_cache:
            return await self.response_cache.get_stats()
        return None

    async def invalidate_cache(self, endpoint: str) -> int:
        """Invalidate cached responses for a specific endpoint."""
        if self.response_cache:
            return await self.response_cache.invalidate_endpoint(endpoint)
        return 0

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        await self.close()
