"""
Pytest configuration and common fixtures for TCGPlayer Client tests.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from tcgplayer_client import TCGPlayerClient
from tcgplayer_client.auth import TCGPlayerAuth
from tcgplayer_client.rate_limiter import RateLimiter


class MockAsyncContextManager:
    """Mock class that properly simulates async context manager behavior."""

    def __init__(self, mock_response):
        self.mock_response = mock_response

    async def __aenter__(self):
        return self.mock_response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp ClientSession for testing."""
    session = AsyncMock()
    session.get = AsyncMock()
    session.post = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def mock_rate_limiter():
    """Mock rate limiter for testing."""
    limiter = MagicMock(spec=RateLimiter)
    limiter.acquire = AsyncMock(return_value=True)
    limiter.release = AsyncMock()
    return limiter


@pytest.fixture
def mock_auth():
    """Mock authentication for testing."""
    auth = MagicMock(spec=TCGPlayerAuth)
    auth.authenticate = AsyncMock(return_value={"access_token": "test_token"})
    auth.access_token = "test_token"
    return auth


@pytest.fixture
def tcgplayer_client(mock_auth, mock_rate_limiter):
    """TCGPlayer client instance with mocked dependencies."""
    client = TCGPlayerClient()
    client.auth = mock_auth
    client.rate_limiter = mock_rate_limiter
    return client


@pytest.fixture
def sample_api_response():
    """Sample API response for testing."""
    return {
        "success": True,
        "errors": [],
        "results": [
            {
                "categoryId": 1,
                "name": "Magic: The Gathering",
                "displayName": "Magic: The Gathering",
                "seoCategoryName": "magic-the-gathering",
            }
        ],
    }


@pytest.fixture
def sample_error_response():
    """Sample error response for testing."""
    return {"success": False, "errors": ["Invalid category ID"], "results": []}


@pytest.fixture
def mock_http_response():
    """Mock HTTP response object for testing."""
    response = AsyncMock()
    response.status = 200
    response.json = AsyncMock(return_value={"success": True, "results": []})
    response.text = AsyncMock(return_value="")
    return response


@pytest.fixture
def mock_aiohttp_client():
    """Mock aiohttp client that properly handles async context managers."""

    def create_mock_session():
        session = AsyncMock()

        # Configure get method
        def mock_get(url, headers=None):
            response = AsyncMock()
            response.status = 200
            response.json = AsyncMock(return_value={"success": True, "results": []})
            response.text = AsyncMock(return_value="")
            return MockAsyncContextManager(response)

        session.get = mock_get

        # Configure post method
        def mock_post(url, data=None, json=None, headers=None):
            response = AsyncMock()
            response.status = 200
            response.json = AsyncMock(return_value={"success": True, "results": []})
            response.text = AsyncMock(return_value="")
            return MockAsyncContextManager(response)

        session.post = mock_post

        return session

    return create_mock_session


# Configure pytest-asyncio
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
