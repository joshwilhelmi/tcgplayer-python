"""
Session management for TCGPlayer API requests.

This module provides efficient HTTP session management with connection pooling,
timeout configuration, and automatic cleanup.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages HTTP sessions with connection pooling and automatic cleanup."""

    def __init__(
        self,
        timeout: Optional[aiohttp.ClientTimeout] = None,
        connector: Optional[aiohttp.BaseConnector] = None,
        max_connections: int = 100,
        max_connections_per_host: int = 10,
        keepalive_timeout: int = 30,
        enable_cleanup_closed: bool = True,
    ) -> None:
        """
        Initialize the session manager.

        Args:
            timeout: Client timeout configuration
            connector: Custom connector (optional)
            max_connections: Maximum total connections
            max_connections_per_host: Maximum connections per host
            keepalive_timeout: Keep-alive timeout in seconds
            enable_cleanup_closed: Enable cleanup of closed connections
        """
        self.timeout = timeout or aiohttp.ClientTimeout(
            total=30,  # 30 seconds total timeout
            connect=10,  # 10 seconds connection timeout
            sock_read=30,  # 30 seconds socket read timeout
        )

        # Store connector configuration for lazy initialization
        self._connector_config = {
            "limit": max_connections,
            "limit_per_host": max_connections_per_host,
            "keepalive_timeout": keepalive_timeout,
            "enable_cleanup_closed": enable_cleanup_closed,
        }

        self._connector = connector  # Use provided connector if available
        self._session: Optional[aiohttp.ClientSession] = None
        self._lock = asyncio.Lock()

        logger.info(
            f"Session manager initialized with max_connections={max_connections}, "
            f"max_per_host={max_connections_per_host}, keepalive={keepalive_timeout}s"
        )

    @property
    def connector(self) -> aiohttp.BaseConnector:
        """Get or create the connector lazily."""
        if self._connector is None:
            try:
                self._connector = aiohttp.TCPConnector(
                    limit=self._connector_config["limit"],
                    limit_per_host=self._connector_config["limit_per_host"],
                    keepalive_timeout=self._connector_config["keepalive_timeout"],
                    enable_cleanup_closed=bool(
                        self._connector_config["enable_cleanup_closed"]
                    ),
                    ttl_dns_cache=300,  # 5 minutes DNS cache
                    use_dns_cache=True,
                )
                logger.debug("Created new TCP connector")
            except RuntimeError:
                # No event loop available, create a basic connector
                logger.debug("No event loop available, creating basic connector")
                self._connector = aiohttp.TCPConnector()

        return self._connector

    async def get_session(self) -> aiohttp.ClientSession:
        """
        Get or create an HTTP session.

        Returns:
            HTTP client session
        """
        if self._session is None or self._session.closed:
            async with self._lock:
                if self._session is None or self._session.closed:
                    self._session = aiohttp.ClientSession(
                        timeout=self.timeout,
                        connector=self.connector,
                        headers={
                            "User-Agent": "TCGPlayer-Python-Client/1.0.0",
                            "Accept": "application/json",
                            "Accept-Encoding": "gzip, deflate",
                        },
                    )
                    logger.debug("Created new HTTP session")

        return self._session

    async def close_session(self) -> None:
        """Close the current session if it exists."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
            logger.debug("Closed HTTP session")

    async def cleanup(self) -> None:
        """Clean up resources."""
        await self.close_session()
        if self._connector:
            await self._connector.close()
            self._connector = None
            logger.debug("Closed connector")

    @asynccontextmanager
    async def session_context(self):
        """
        Context manager for session usage.

        Yields:
            HTTP client session
        """
        session = await self.get_session()
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            # Don't close session on every error, just log it
            raise
        # Session remains open for reuse

    def is_session_active(self) -> bool:
        """Check if the session is active and not closed."""
        return self._session is not None and not self._session.closed

    async def health_check(self) -> bool:
        """
        Perform a health check on the session.

        Returns:
            True if session is healthy, False otherwise
        """
        try:
            session = await self.get_session()
            # Simple health check - try to access a property
            return not session.closed
        except Exception as e:
            logger.warning(f"Session health check failed: {e}")
            return False
