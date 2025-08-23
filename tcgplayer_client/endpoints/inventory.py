"""
Inventory endpoints for TCGPlayer API.

This module contains all inventory-related operations including:
- Product lists and management
- Inventory quantity and pricing
- Product relationships
"""

from typing import Any, Dict, List

from ..client import TCGPlayerClient


class InventoryEndpoints:
    """Inventory-related API endpoints."""

    def __init__(self, client: TCGPlayerClient):
        """
        Initialize inventory endpoints.

        Args:
            client: TCGPlayer client instance
        """
        self.client = client

    async def get_productlist_by_id(self, productlist_id: int) -> Dict[str, Any]:
        """Get product list by ID."""
        return await self.client._make_api_request(
            f"/inventory/productlists/{productlist_id}"
        )

    async def get_productlist_by_key(self, productlist_key: str) -> Dict[str, Any]:
        """Get product list by key."""
        return await self.client._make_api_request(
            f"/inventory/productlists/key/{productlist_key}"
        )

    async def list_all_productlists(self) -> Dict[str, Any]:
        """List all product lists."""
        return await self.client._make_api_request("/inventory/productlists")

    async def create_productlist(
        self, productlist_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new product list."""
        return await self.client._make_api_request(
            "/inventory/productlists", method="POST", data=productlist_data
        )

    async def get_store_product_summary(
        self, store_id: int, product_id: int
    ) -> Dict[str, Any]:
        """Get store product summary."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/products/{product_id}"
        )

    async def get_store_product_skus(
        self, store_id: int, product_id: int
    ) -> Dict[str, Any]:
        """Get store product SKUs."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/products/{product_id}/skus"
        )

    async def get_store_related_products(
        self, store_id: int, product_id: int
    ) -> Dict[str, Any]:
        """Get store related products."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/products/{product_id}/related"
        )

    async def get_store_sku_quantity(
        self, store_id: int, sku_id: int
    ) -> Dict[str, Any]:
        """Get store SKU quantity."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/inventory/{sku_id}"
        )

    async def increment_sku_inventory_quantity(
        self, store_id: int, sku_id: int, quantity: int
    ) -> Dict[str, Any]:
        """Increment SKU inventory quantity."""
        data = {"quantity": quantity}
        return await self.client._make_api_request(
            f"/stores/{store_id}/inventory/{sku_id}/increment", method="POST", data=data
        )

    async def update_sku_inventory(
        self, store_id: int, sku_id: int, quantity: int
    ) -> Dict[str, Any]:
        """Update SKU inventory quantity."""
        data = {"quantity": quantity}
        return await self.client._make_api_request(
            f"/stores/{store_id}/inventory/{sku_id}", method="PUT", data=data
        )

    async def batch_update_store_sku_prices(
        self, store_id: int, price_updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Batch update store SKU prices."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/prices/skus", method="POST", data=price_updates
        )

    async def update_sku_inventory_price(
        self, store_id: int, sku_id: int, price: float
    ) -> Dict[str, Any]:
        """Update SKU inventory price."""
        data = {"price": price}
        return await self.client._make_api_request(
            f"/stores/{store_id}/inventory/{sku_id}/price", method="PUT", data=data
        )

    async def list_sku_list_price(self, store_id: int, sku_id: int) -> Dict[str, Any]:
        """List SKU list price."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/inventory/{sku_id}/list"
        )

    async def get_sku_list_price(self, store_id: int, sku_id: int) -> Dict[str, Any]:
        """Get SKU list price."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/inventory/{sku_id}/list"
        )
