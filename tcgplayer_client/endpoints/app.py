"""
App endpoints for TCGplayer API.

This module contains application-level operations including:
- Application authorization and key management
"""

from typing import Any, Dict

from ..client import TCGplayerClient


class AppEndpoints:
    """Application-level API endpoints."""

    def __init__(self, client: "TCGplayerClient"):
        """
        Initialize app endpoints.

        Args:
            client: TCGplayer client instance
        """
        self.client = client

    async def authorize_application(self, auth_code: str) -> Dict[str, Any]:
        """
        Create an application key based on a previously generated authorization code.

        This endpoint authorizes an application using an OAuth authorization code,
        returning an application key that can be used for API access.

        Args:
            auth_code: Authorization code generated from OAuth

        Returns:
            Dict containing the application authorization response

        Raises:
            ValueError: If auth_code is empty or None
            APIError: If the API request fails (400: Invalid code, 404: Code not found)

        Example:
            >>> app_endpoints = AppEndpoints(client)
            >>> result = await app_endpoints.authorize_application("abc123xyz")
            >>> print(result)  # Application key and authorization details
        """
        if not auth_code or not auth_code.strip():
            raise ValueError("auth_code cannot be empty or None")

        return await self.client._make_api_request(
            f"/app/authorize/{auth_code.strip()}", method="POST"
        )
