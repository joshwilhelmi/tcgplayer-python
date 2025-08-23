"""
Rate limiter implementation for TCGPlayer API requests.
"""

import asyncio
import logging
import time
from collections import deque
from typing import Deque

logger = logging.getLogger(__name__)

# TCGPlayer API absolute maximum rate limit
# Exceeding this can result in API access being revoked
MAX_REQUESTS_PER_SECOND = 10


class RateLimiter:
    """Rate limiter to respect TCGPlayer's API rate limits."""

    def __init__(self, max_requests: int = 10, time_window: float = 1.0) -> None:
        """
        Initialize the rate limiter.

        Args:
            max_requests: Maximum number of requests allowed in the time window
            time_window: Time window in seconds

        Raises:
            ValueError: If max_requests exceeds the absolute maximum of 10
        """
        # Enforce absolute maximum rate limit
        if max_requests > MAX_REQUESTS_PER_SECOND:
            logger.warning(
                f"Requested rate limit {max_requests} req/s exceeds TCGPlayer's "
                f"maximum of {MAX_REQUESTS_PER_SECOND} req/s. "
                f"Rate limit has been capped to {MAX_REQUESTS_PER_SECOND} req/s "
                f"to prevent API violations."
            )
            max_requests = MAX_REQUESTS_PER_SECOND

        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Deque[float] = deque()
        self.lock = asyncio.Lock()

        logger.info(
            f"Rate limiter configured: {max_requests} requests per {time_window} "
            f"second(s) (TCGPlayer maximum: {MAX_REQUESTS_PER_SECOND} req/s)"
        )

    async def acquire(self) -> None:
        """
        Acquire permission to make a request, waiting if necessary.

        This method will block until a request slot is available.
        """
        async with self.lock:
            now = time.time()

            # Remove expired requests
            while self.requests and self.requests[0] <= now - self.time_window:
                self.requests.popleft()

            # If at rate limit, wait until we can make another request
            if len(self.requests) >= self.max_requests:
                wait_time = self.requests[0] - (now - self.time_window)
                if wait_time > 0:
                    logger.info(
                        f"Rate limit reached. Waiting {wait_time:.2f} seconds..."
                    )
                    await asyncio.sleep(wait_time)
                    now = time.time()

            # Record this request
            self.requests.append(now)
            logger.debug(
                f"Request allowed. Current rate: "
                f"{len(self.requests)}/{self.max_requests} "
                f"per {self.time_window}s"
            )

    def get_status(self) -> dict:
        """
        Get current rate limiter status.

        Returns:
            Dictionary with current rate limiter state
        """

        async def _get_status():
            async with self.lock:
                current_requests = len(self.requests)
                max_requests = self.max_requests
                time_window = self.time_window

                return {
                    "current_requests": current_requests,
                    "max_requests_per_window": max_requests,
                    "time_window_seconds": time_window,
                    "remaining_requests": max(0, max_requests - current_requests),
                    "rate_limit_reset_in_seconds": (
                        time_window if current_requests >= max_requests else 0
                    ),
                }

        # Create a new event loop if one doesn't exist (for sync access)
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're in an async context, we can't run this synchronously
                # Return a placeholder that indicates async access is required
                return {
                    "error": "Cannot get status synchronously from async context. "
                    "Use get_status_async() instead."
                }
            else:
                return loop.run_until_complete(_get_status())
        except RuntimeError:
            # No event loop, create a new one
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(_get_status())
            finally:
                loop.close()

    async def get_status_async(self) -> dict:
        """
        Get current rate limiter status asynchronously.

        Returns:
            Dictionary with current rate limiter state
        """
        async with self.lock:
            current_requests = len(self.requests)
            max_requests = self.max_requests
            time_window = self.time_window

            return {
                "current_requests": current_requests,
                "max_requests_per_window": max_requests,
                "time_window_seconds": time_window,
                "remaining_requests": max(0, max_requests - current_requests),
                "rate_limit_reset_in_seconds": (
                    time_window if current_requests >= max_requests else 0
                ),
            }
