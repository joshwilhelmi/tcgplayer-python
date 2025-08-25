"""
Authentication handling for TCGPlayer API.
"""

import logging
import os
from typing import Any, Dict, Optional

import aiohttp

from .exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class TCGPlayerAuth:
    """Handles authentication with the TCGPlayer API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        base_url: str = "https://api.tcgplayer.com",
    ) -> None:
        """
        Initialize the authentication handler.

        Args:
            client_id: TCGPlayer API client ID (defaults to TCGPLAYER_CLIENT_ID env var)
            client_secret: TCGPlayer API client secret (defaults to
            TCGPLAYER_CLIENT_SECRET env var)
            base_url: Base URL for TCGPlayer API (defaults to production API)
        """
        self.client_id = client_id or os.getenv("TCGPLAYER_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("TCGPLAYER_CLIENT_SECRET")
        self.base_url = base_url
        self.access_token: Optional[str] = None

        # For testing purposes, allow empty credentials but log a warning
        if not self.client_id or not self.client_secret:
            logger.warning(
                "TCGPLAYER_CLIENT_ID and TCGPLAYER_CLIENT_SECRET not provided. "
                "Authentication will not be available."
            )

    async def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate with TCGPlayer API using client credentials.

        Returns:
            Dictionary containing authentication result

        Raises:
            AuthenticationError: If authentication fails
        """
        if not self.client_id or not self.client_secret:
            raise AuthenticationError("No credentials available for authentication")

        auth_url = f"{self.base_url}/token"
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(auth_url, data=auth_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.access_token = result.get("access_token")

                        if self.access_token:
                            logger.info("Successfully authenticated with TCGPlayer API")
                            return {
                                "success": True,
                                "message": "Authentication successful",
                                "access_token": self.access_token,
                            }
                        else:
                            raise AuthenticationError(
                                "No access token received from TCGPlayer API"
                            )
                    else:
                        error_text = await response.text()
                        raise AuthenticationError(
                            f"Authentication failed: {response.status} - {error_text}"
                        )
        except aiohttp.ClientError as e:
            raise AuthenticationError(f"Network error during authentication: {e}")
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise AuthenticationError(f"Authentication failed: {e}")

    def get_access_token(self) -> Optional[str]:
        """
        Get the current access token.

        Returns:
            Current access token or None if not authenticated
        """
        return self.access_token

    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        return self.access_token is not None

    async def get_store_bearer_token(self, access_token: str) -> Dict[str, Any]:
        """
        Get a bearer token for store access using an access token.

        POST to: https://api.tcgplayer.com/token/access
        Headers: X-Tcg-Access-Token: {access_token}

        Args:
            access_token: The access token received from store authorization

        Returns:
            Dictionary containing the bearer token result

        Raises:
            AuthenticationError: If token exchange fails
        """
        if not access_token:
            raise AuthenticationError(
                "Access token is required for store authorization"
            )

        token_url = f"{self.base_url}/token/access"
        headers = {"X-Tcg-Access-Token": access_token}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(token_url, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        bearer_token = result.get("access_token")

                        if bearer_token:
                            logger.info("Successfully obtained store bearer token")
                            return {
                                "success": True,
                                "message": "Store bearer token obtained successfully",
                                "bearer_token": bearer_token,
                                "token_type": result.get("token_type", "bearer"),
                                "expires_in": result.get("expires_in"),
                            }
                        else:
                            raise AuthenticationError(
                                "No bearer token received from TCGPlayer API"
                            )
                    else:
                        error_text = await response.text()
                        raise AuthenticationError(
                            f"Token exchange failed: {response.status} - {error_text}"
                        )
        except aiohttp.ClientError as e:
            raise AuthenticationError(f"Network error during token exchange: {e}")
        except Exception as e:
            logger.error(f"Token exchange error: {e}")
            raise AuthenticationError(f"Token exchange failed: {e}")

    def clear_token(self) -> None:
        """Clear the current access token."""
        self.access_token = None
        logger.info("Access token cleared")
