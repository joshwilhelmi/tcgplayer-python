"""
Buylist endpoints for TCGPlayer API.

This module contains all buylist-related operations including:
- Store buylist management
- Buylist pricing and quantities
- Buylist categories and groups
"""

from typing import Any, Dict, List, Optional

from ..client import TCGPlayerClient


class BuylistEndpoints:
    """Buylist-related API endpoints."""

    def __init__(self, client: TCGPlayerClient):
        """
        Initialize buylist endpoints.

        Args:
            client: TCGPlayer client instance
        """
        self.client = client

    async def batch_update_store_buylist_prices(
        self, store_id: int, price_updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Batch update store buylist prices."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/buylist/prices", method="POST", data=price_updates
        )

    async def create_sku_buylist(
        self, store_id: int, buylist_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new SKU buylist entry."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/buylist/skus", method="POST", data=buylist_data
        )

    async def update_sku_buylist_price(
        self, store_id: int, sku_id: int, price: float
    ) -> Dict[str, Any]:
        """Update SKU buylist price."""
        data = {"price": price}
        return await self.client._make_api_request(
            f"/stores/{store_id}/buylist/skus/{sku_id}/price", method="PUT", data=data
        )

    async def update_sku_buylist_quantity(
        self, store_id: int, sku_id: int, quantity: float
    ) -> Dict[str, Any]:
        """Update SKU buylist quantity."""
        data = {"quantity": quantity}
        return await self.client._make_api_request(
            f"/stores/{store_id}/buylist/skus/{sku_id}/quantity",
            method="PUT",
            data=data,
        )

    async def get_buylist_categories(self, store_id: int) -> Dict[str, Any]:
        """Get buylist categories for a store."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/buylist/categories"
        )

    async def get_buylist_groups(self, store_id: int) -> Dict[str, Any]:
        """Get buylist groups for a store."""
        return await self.client._make_api_request(f"/stores/{store_id}/buylist/groups")

    async def get_store_buylist_settings(self, store_id: int) -> Dict[str, Any]:
        """Get store buylist settings."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/buylist/settings"
        )

    async def get_store_buylist_products_kiosk(self, store_id: int) -> Dict[str, Any]:
        """Get store buylist products for kiosk display."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/buylist/products/kiosk"
        )

    async def get_buylist_product_conditions(self, store_id: int) -> Dict[str, Any]:
        """Get buylist product conditions for a store."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/buylist/conditions"
        )
