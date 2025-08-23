"""
Store endpoints for TCGPlayer API.

This module contains all store-related operations including:
- Store management and settings
- Customer management
- Product inventory and pricing
- Shipping and feedback
"""

from typing import Any, Dict, List, Optional

from ..client import TCGPlayerClient


class StoreEndpoints:
    """Store-related API endpoints."""

    def __init__(self, client: TCGPlayerClient):
        """
        Initialize store endpoints.

        Args:
            client: TCGPlayer client instance
        """
        self.client = client

    async def get_free_shipping_option(self, store_id: int) -> Dict[str, Any]:
        """Get free shipping option for a store."""
        return await self.client._make_api_request(f"/stores/{store_id}/shipping/free")

    async def get_store_address(self, store_id: int) -> Dict[str, Any]:
        """Get store address information."""
        return await self.client._make_api_request(f"/stores/{store_id}/address")

    async def get_store_feedback(self, store_id: int) -> Dict[str, Any]:
        """Get store feedback information."""
        return await self.client._make_api_request(f"/stores/{store_id}/feedback")

    async def set_store_status(self, store_id: int, status: str) -> Dict[str, Any]:
        """Set store status (open/closed)."""
        data = {"status": status}
        return await self.client._make_api_request(
            f"/stores/{store_id}/status", method="PUT", data=data
        )

    async def get_customer_summary(
        self, store_id: int, customer_id: int
    ) -> Dict[str, Any]:
        """Get customer summary for a store."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/customers/{customer_id}"
        )

    async def search_store_customers(
        self, store_id: int, search_term: str
    ) -> Dict[str, Any]:
        """Search for customers in a store."""
        params = {"term": search_term}
        return await self.client._make_api_request(
            f"/stores/{store_id}/customers/search", params=params
        )

    async def get_customer_addresses(
        self, store_id: int, customer_id: int
    ) -> Dict[str, Any]:
        """Get customer addresses for a store."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/customers/{customer_id}/addresses"
        )

    async def get_customer_orders(
        self, store_id: int, customer_id: int
    ) -> Dict[str, Any]:
        """Get customer orders for a store."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/customers/{customer_id}/orders"
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

    async def get_store_shipping_options(self, store_id: int) -> Dict[str, Any]:
        """Get store shipping options."""
        return await self.client._make_api_request(f"/stores/{store_id}/shipping")

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

    async def get_store_groups(self, store_id: int) -> Dict[str, Any]:
        """Get store groups."""
        return await self.client._make_api_request(f"/stores/{store_id}/groups")

    async def get_store_categories(self, store_id: int) -> Dict[str, Any]:
        """Get store categories."""
        return await self.client._make_api_request(f"/stores/{store_id}/categories")

    async def search_custom_listings(
        self, store_id: int, search_term: str
    ) -> Dict[str, Any]:
        """Search custom listings in a store."""
        params = {"term": search_term}
        return await self.client._make_api_request(
            f"/stores/{store_id}/listings/search", params=params
        )
