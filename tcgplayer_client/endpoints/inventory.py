"""
Inventory endpoints for TCGplayer API.

This module contains product list management operations:
- Get product list by ID or key
- List all product lists
- Create new product lists
"""

from typing import Any, Dict, Optional

from ..client import TCGplayerClient


class InventoryEndpoints:
    """Product list management API endpoints."""

    def __init__(self, client: TCGplayerClient):
        """
        Initialize inventory endpoints.

        Args:
            client: TCGplayer client instance
        """
        self.client = client

    async def get_productlist_by_id(self, product_list_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific product list by ID.

        Args:
            product_list_id: Integer ID of the product list to retrieve

        Returns:
            Dict containing product list details with items, ID, key, and creation date
        """
        return await self.client._make_api_request(
            f"/inventory/productlists/{product_list_id}"
        )

    async def get_productlist_by_key(self, product_list_key: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific product list by key.

        Args:
            product_list_key: Unique identifier for the product list

        Returns:
            Dict containing product list details with items, ID, key, and creation date
        """
        return await self.client._make_api_request(
            f"/inventory/productlists/{product_list_key}"
        )

    async def list_all_productlists(self) -> Dict[str, Any]:
        """
        List all accessible product lists for the authenticated user.

        Returns:
            Dict containing array of product lists with ID, key, and creation date
        """
        return await self.client._make_api_request("/inventory/productLists")

    async def create_productlist(
        self, product_list_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new product list similar to how the Quicklist application
        creates lists.

        Args:
            product_list_data: Optional product list configuration data

        Returns:
            Dict containing the newly created product list key

        Note:
            Requires specific permissions - not accessible by all users
        """
        return await self.client._make_api_request(
            "/inventory/productLists", method="POST", data=product_list_data
        )
