"""
Store endpoints for TCGPlayer API.

This module contains all store-related operations including:
- Store management and settings
- Customer management
- Product inventory and pricing
- Shipping and feedback
- Store authorization workflow
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

    async def authorize_application(self, authorization_code: str) -> Dict[str, Any]:
        """
        Authorize an application with a store using authorization code.

        POST to: https://api.tcgplayer.com/app/authorize/{authCode}
        """
        return await self.client._make_api_request(
            f"/app/authorize/{authorization_code}", method="POST"
        )

    async def get_store_self(self) -> Dict[str, Any]:
        """
        Get the identity of the TCGPlayer store using the current bearer token.

        GET: https://api.tcgplayer.com/stores/self
        Headers: Authorization: Bearer {BEARER_TOKEN}
        """
        return await self.client._make_api_request("/stores/self")

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

    async def get_store_product_related_products(
        self, store_id: int, product_id: int
    ) -> Dict[str, Any]:
        """Get store related products for a specific product."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/products/{product_id}/related"
        )

    async def get_store_shipping_options_by_id(self, store_id: int) -> Dict[str, Any]:
        """Get store shipping options by store ID."""
        return await self.client._make_api_request(f"/stores/{store_id}/shipping")

    async def get_store_sku_quantity_by_id(
        self, store_id: int, sku_id: int
    ) -> Dict[str, Any]:
        """Get store SKU quantity by store ID."""
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

    async def batch_update_store_sku_prices_by_id(
        self, store_id: int, price_updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Batch update store SKU prices by store ID."""
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

    async def get_store_groups_by_id(self, store_id: int) -> Dict[str, Any]:
        """Get store groups by store ID."""
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

    # Store endpoints using storeKey (for authorized store access)
    async def get_store_inventory_quantities(self, store_key: str) -> Dict[str, Any]:
        """Get product inventory quantities for a store using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/quantities"
        )

    async def get_store_products_summary(self, store_key: str) -> Dict[str, Any]:
        """Get store products summary using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/products/summary"
        )

    async def get_store_products_skus(self, store_key: str) -> Dict[str, Any]:
        """Get store product SKUs using storeKey."""
        return await self.client._make_api_request(f"/stores/{store_key}/products/skus")

    async def get_store_related_products(self, store_key: str) -> Dict[str, Any]:
        """Get store related products using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/products/related"
        )

    async def get_store_shipping_options(self, store_key: str) -> Dict[str, Any]:
        """Get store shipping options using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/shipping/options"
        )

    async def get_store_sku_quantity(
        self, store_key: str, sku_id: int
    ) -> Dict[str, Any]:
        """Get store SKU quantity using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/sku/{sku_id}/quantity"
        )

    async def increment_store_sku_quantity(
        self, store_key: str, sku_id: int, quantity: int
    ) -> Dict[str, Any]:
        """Increment store SKU quantity using storeKey."""
        data = {"quantity": quantity}
        return await self.client._make_api_request(
            f"/stores/{store_key}/sku/{sku_id}/quantity/increment",
            method="POST",
            data=data,
        )

    async def update_store_sku_inventory(
        self, store_key: str, sku_id: int, quantity: int
    ) -> Dict[str, Any]:
        """Update store SKU inventory using storeKey."""
        data = {"quantity": quantity}
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/sku", method="PUT", data=data
        )

    async def batch_update_store_sku_prices(
        self, store_key: str, price_updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Batch update store SKU prices using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/prices/batch", method="POST", data=price_updates
        )

    async def update_store_sku_price(
        self, store_key: str, sku_id: int, price: float
    ) -> Dict[str, Any]:
        """Update store SKU price using storeKey."""
        data = {"price": price}
        return await self.client._make_api_request(
            f"/stores/{store_key}/sku/{sku_id}/price", method="PUT", data=data
        )

    async def get_store_sku_list_price(
        self, store_key: str, sku_id: int
    ) -> Dict[str, Any]:
        """Get store SKU list price using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/sku/{sku_id}/price"
        )

    async def get_store_groups(self, store_key: str) -> Dict[str, Any]:
        """Get store groups using storeKey."""
        return await self.client._make_api_request(f"/stores/{store_key}/groups")

    async def get_store_categories_by_key(self, store_key: str) -> Dict[str, Any]:
        """Get store categories using storeKey."""
        return await self.client._make_api_request(f"/stores/{store_key}/categories")

    async def search_store_custom_listings(
        self, store_key: str, search_term: str
    ) -> Dict[str, Any]:
        """Search custom listings in a store using storeKey."""
        params = {"term": search_term}
        return await self.client._make_api_request(
            f"/stores/{store_key}/listings/custom/search", params=params
        )

    async def get_store_order_manifest(self, store_key: str) -> Dict[str, Any]:
        """Get store order manifest using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/manifest"
        )

    async def get_store_order_details(
        self, store_key: str, order_id: int
    ) -> Dict[str, Any]:
        """Get store order details using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_id}"
        )

    async def get_store_order_feedback(
        self, store_key: str, order_id: int
    ) -> Dict[str, Any]:
        """Get store order feedback using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_id}/feedback"
        )

    async def search_store_orders(
        self, store_key: str, search_term: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search store orders using storeKey."""
        params = {}
        if search_term:
            params["term"] = search_term
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders", params=params
        )

    async def get_store_order_items(
        self, store_key: str, order_id: int
    ) -> Dict[str, Any]:
        """Get store order items using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_id}/items"
        )

    async def get_store_order_tracking(
        self, store_key: str, order_id: int
    ) -> Dict[str, Any]:
        """Get store order tracking using storeKey."""
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_id}/tracking"
        )

    async def add_store_order_tracking(
        self, store_key: str, order_id: int, tracking_number: str
    ) -> Dict[str, Any]:
        """Add store order tracking using storeKey."""
        data = {"trackingNumber": tracking_number}
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_id}/tracking", method="POST", data=data
        )
