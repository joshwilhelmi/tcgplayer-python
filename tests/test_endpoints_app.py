"""
Tests for App endpoints.
"""

import pytest
from unittest.mock import AsyncMock, Mock
from tcgplayer_client.endpoints.app import AppEndpoints
from tcgplayer_client.exceptions import APIError


class TestAppEndpoints:
    """Test suite for App endpoints."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_client._make_api_request = AsyncMock()
        self.app_endpoints = AppEndpoints(self.mock_client)

    @pytest.mark.asyncio
    async def test_authorize_application_success(self):
        """Test successful application authorization."""
        # Arrange
        auth_code = "test_auth_code_12345"
        expected_response = {
            "success": True,
            "application_key": "app_key_67890",
            "expires_in": 3600
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.app_endpoints.authorize_application(auth_code)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            f"/app/authorize/{auth_code}", 
            method="POST"
        )

    @pytest.mark.asyncio
    async def test_authorize_application_with_whitespace(self):
        """Test application authorization with whitespace in auth code."""
        # Arrange
        auth_code = "  test_auth_code_12345  "
        expected_response = {"success": True}
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.app_endpoints.authorize_application(auth_code)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/app/authorize/test_auth_code_12345",  # Should be trimmed
            method="POST"
        )

    @pytest.mark.asyncio
    async def test_authorize_application_empty_auth_code(self):
        """Test application authorization with empty auth code raises ValueError."""
        # Test empty string
        with pytest.raises(ValueError, match="auth_code cannot be empty or None"):
            await self.app_endpoints.authorize_application("")

        # Test None
        with pytest.raises(ValueError, match="auth_code cannot be empty or None"):
            await self.app_endpoints.authorize_application(None)

        # Test whitespace only
        with pytest.raises(ValueError, match="auth_code cannot be empty or None"):
            await self.app_endpoints.authorize_application("   ")

    @pytest.mark.asyncio
    async def test_authorize_application_api_error(self):
        """Test application authorization with API error."""
        # Arrange
        auth_code = "invalid_auth_code"
        self.mock_client._make_api_request.side_effect = APIError(
            "Invalid authorization code submitted", 
            status_code=400
        )

        # Act & Assert
        with pytest.raises(APIError) as exc_info:
            await self.app_endpoints.authorize_application(auth_code)
        
        assert exc_info.value.status_code == 400
        assert "Invalid authorization code" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_authorize_application_not_found_error(self):
        """Test application authorization with not found error."""
        # Arrange
        auth_code = "nonexistent_auth_code"
        self.mock_client._make_api_request.side_effect = APIError(
            "Submitted authorization code not found",
            status_code=404
        )

        # Act & Assert
        with pytest.raises(APIError) as exc_info:
            await self.app_endpoints.authorize_application(auth_code)
        
        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value)

    def test_app_endpoints_initialization(self):
        """Test AppEndpoints initialization."""
        # Test that client is properly stored
        assert self.app_endpoints.client == self.mock_client
        
        # Test that authorize_application method exists
        assert hasattr(self.app_endpoints, 'authorize_application')
        assert callable(self.app_endpoints.authorize_application)