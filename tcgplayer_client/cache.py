"""
Caching layer for TCGPlayer Client.

This module provides response caching with TTL management,
LRU eviction, and configurable cache policies.
"""

import asyncio
import hashlib
import json
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CacheEntry:
    """Represents a cached item."""

    key: str
    value: Any
    timestamp: float = field(default_factory=time.time)
    ttl: int = 300  # 5 minutes default
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)

    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        return time.time() - self.timestamp > self.ttl

    def access(self):
        """Mark the entry as accessed."""
        self.access_count += 1
        self.last_accessed = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "key": self.key,
            "value": self.value,
            "timestamp": self.timestamp,
            "ttl": self.ttl,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
        }


class CacheKeyGenerator:
    """Generates cache keys for API requests."""

    @staticmethod
    def generate_key(
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        data: Optional[Any] = None,
    ) -> str:
        """
        Generate a cache key for an API request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            method: HTTP method
            data: Request body data

        Returns:
            Cache key string
        """
        # Create a unique identifier for the request
        key_parts = [method, endpoint]

        if params:
            # Sort parameters for consistent key generation
            sorted_params = sorted(params.items())
            key_parts.append(json.dumps(sorted_params, sort_keys=True))

        if data:
            key_parts.append(json.dumps(data, sort_keys=True))

        # Create hash of the key parts using SHA256 for security
        key_string = "|".join(str(part) for part in key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()

    @staticmethod
    def generate_user_key(user_id: str, endpoint: str, **kwargs) -> str:
        """Generate a user-specific cache key."""
        base_key = CacheKeyGenerator.generate_key(endpoint, **kwargs)
        return f"user:{user_id}:{base_key}"


class LRUCache:
    """LRU (Least Recently Used) cache implementation."""

    def __init__(self, max_size: int = 1000):
        """
        Initialize LRU cache.

        Args:
            max_size: Maximum number of cache entries
        """
        self.max_size = max_size
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        async with self._lock:
            if key in self.cache:
                entry = self.cache[key]

                # Check if expired
                if entry.is_expired():
                    del self.cache[key]
                    return None

                # Mark as accessed and move to end (most recently used)
                entry.access()
                self.cache.move_to_end(key)
                return entry.value

            return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """
        Set a value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        """
        async with self._lock:
            # Create new entry
            entry = CacheEntry(key=key, value=value, ttl=ttl)

            # If key exists, remove old entry
            if key in self.cache:
                del self.cache[key]

            # Add new entry
            self.cache[key] = entry

            # Evict oldest entries if cache is full
            while len(self.cache) > self.max_size:
                self.cache.popitem(last=False)

    async def delete(self, key: str) -> bool:
        """
        Delete a key from cache.

        Args:
            key: Cache key to delete

        Returns:
            True if key was deleted, False if not found
        """
        async with self._lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False

    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self.cache.clear()

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        async with self._lock:
            total_entries = len(self.cache)
            expired_entries = sum(
                1 for entry in self.cache.values() if entry.is_expired()
            )
            active_entries = total_entries - expired_entries

            # Calculate average TTL and access count
            if active_entries > 0:
                avg_ttl = (
                    sum(
                        entry.ttl
                        for entry in self.cache.values()
                        if not entry.is_expired()
                    )
                    / active_entries
                )
                avg_access = (
                    sum(
                        entry.access_count
                        for entry in self.cache.values()
                        if not entry.is_expired()
                    )
                    / active_entries
                )
            else:
                avg_ttl = 0
                avg_access = 0

            return {
                "total_entries": total_entries,
                "active_entries": active_entries,
                "expired_entries": expired_entries,
                "max_size": self.max_size,
                "utilization": (total_entries / self.max_size) * 100,
                "average_ttl": avg_ttl,
                "average_access_count": avg_access,
            }

    async def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache.

        Returns:
            Number of entries removed
        """
        async with self._lock:
            expired_keys = [
                key for key, entry in self.cache.items() if entry.is_expired()
            ]

            for key in expired_keys:
                del self.cache[key]

            return len(expired_keys)


class ResponseCache:
    """Caches API responses with configurable policies."""

    def __init__(
        self,
        max_size: int = 1000,
        default_ttl: int = 300,
        enable_compression: bool = False,
    ):
        """
        Initialize response cache.

        Args:
            max_size: Maximum cache size
            default_ttl: Default time to live in seconds
            enable_compression: Whether to enable response compression
        """
        self.cache = LRUCache(max_size)
        self.default_ttl = default_ttl
        self.enable_compression = enable_compression
        self.key_generator = CacheKeyGenerator()

        # Cache policies
        self.cacheable_methods = {"GET"}
        self.cacheable_status_codes = {200, 201, 202}

        # Start cleanup task
        self._cleanup_task = None
        # Don't start cleanup task during initialization to avoid event loop issues
        # It will be started when first needed

    def _start_cleanup_task(self):
        """Start background cleanup task."""

        async def cleanup_loop():
            while True:
                try:
                    await asyncio.sleep(60)  # Run every minute
                    await self.cache.cleanup_expired()
                except Exception as e:
                    # Log error but continue cleanup
                    # Note: In production, you might want to use a proper logger
                    print(f"Cache cleanup error (continuing): {e}")

        self._cleanup_task = asyncio.create_task(cleanup_loop())

    def stop_cleanup_task(self):
        """Stop the background cleanup task."""
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()

    def is_cacheable(self, method: str, status_code: int, endpoint: str) -> bool:
        """
        Check if a response is cacheable.

        Args:
            method: HTTP method
            status_code: HTTP status code
            endpoint: API endpoint

        Returns:
            True if response should be cached
        """
        # Check method
        if method not in self.cacheable_methods:
            return False

        # Check status code
        if status_code not in self.cacheable_status_codes:
            return False

        # Check endpoint (some endpoints shouldn't be cached)
        non_cacheable_endpoints = {
            "/auth/token",  # Authentication tokens
            "/orders",  # Order-related endpoints
            "/inventory",  # Inventory updates
        }

        if any(endpoint.startswith(ep) for ep in non_cacheable_endpoints):
            return False

        return True

    async def get_cached_response(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        data: Optional[Any] = None,
    ) -> Optional[Any]:
        # Start cleanup task if not already started
        if self._cleanup_task is None:
            self._start_cleanup_task()

        """
        Get cached response if available.

        Args:
            endpoint: API endpoint
            params: Query parameters
            method: HTTP method
            data: Request body data

        Returns:
            Cached response or None
        """
        key = self.key_generator.generate_key(endpoint, params, method, data)
        return await self.cache.get(key)

    async def cache_response(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        data: Optional[Any] = None,
        response: Any = None,
        status_code: int = 200,
        custom_ttl: Optional[int] = None,
    ) -> bool:
        # Start cleanup task if not already started
        if self._cleanup_task is None:
            self._start_cleanup_task()
        """
        Cache a response if it's cacheable.

        Args:
            endpoint: API endpoint
            params: Query parameters
            method: HTTP method
            data: Request body data
            response: Response to cache
            status_code: HTTP status code
            custom_ttl: Custom TTL override

        Returns:
            True if response was cached, False otherwise
        """
        if not self.is_cacheable(method, status_code, endpoint):
            return False

        key = self.key_generator.generate_key(endpoint, params, method, data)
        ttl = custom_ttl or self.default_ttl

        await self.cache.set(key, response, ttl)
        return True

    async def invalidate_endpoint(self, endpoint: str) -> int:
        """
        Invalidate all cached responses for an endpoint.

        Args:
            endpoint: Endpoint to invalidate

        Returns:
            Number of entries invalidated
        """
        # This is a simplified implementation
        # In a real implementation, you'd want more sophisticated invalidation
        # For now, we'll clear the entire cache
        await self.cache.clear()
        return 1

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return await self.cache.get_stats()

    async def clear(self) -> None:
        """Clear all cached responses."""
        await self.cache.clear()

    async def close(self) -> None:
        """Clean up cache resources."""
        self.stop_cleanup_task()
        await self.clear()


class CacheManager:
    """Manages multiple cache instances and policies."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize cache manager.

        Args:
            config: Cache configuration
        """
        self.config = config or {}
        self.caches: Dict[str, ResponseCache] = {}
        self._default_cache: Optional[ResponseCache] = None

    def get_cache(self, name: str = "default") -> ResponseCache:
        """
        Get or create a cache instance.

        Args:
            name: Cache name

        Returns:
            ResponseCache instance
        """
        if name not in self.caches:
            # Create new cache with configuration
            cache_config = self.config.get(name, {})
            max_size = cache_config.get("max_size", 1000)
            default_ttl = cache_config.get("default_ttl", 300)
            enable_compression = cache_config.get("enable_compression", False)

            self.caches[name] = ResponseCache(
                max_size=max_size,
                default_ttl=default_ttl,
                enable_compression=enable_compression,
            )

        return self.caches[name]

    def get_default_cache(self) -> ResponseCache:
        """Get the default cache instance."""
        if self._default_cache is None:
            self._default_cache = self.get_cache("default")
        if self._default_cache is None:
            raise RuntimeError("Default cache not initialized")
        return self._default_cache

    async def clear_all(self) -> None:
        """Clear all caches."""
        for cache in self.caches.values():
            await cache.clear()

    async def close_all(self) -> None:
        """Close all caches."""
        for cache in self.caches.values():
            await cache.close()
        self.caches.clear()
        self._default_cache = None

    def get_cache_names(self) -> List[str]:
        """Get list of cache names."""
        return list(self.caches.keys())

    async def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all caches."""
        stats = {}
        for name, cache in self.caches.items():
            stats[name] = await cache.get_stats()
        return stats
