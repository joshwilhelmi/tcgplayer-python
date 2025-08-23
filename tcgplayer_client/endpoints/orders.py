"""
Order endpoints for TCGPlayer API.

This module contains all order-related operations including:
- Order retrieval and search
- Order details and items
- Order feedback and tracking
"""

from typing import Any, Dict, Optional

from ..client import TCGPlayerClient


class OrderEndpoints:
    """Order-related API endpoints."""

    def __init__(self, client: TCGPlayerClient):
        """
        Initialize order endpoints.

        Args:
            client: TCGPlayer client instance
        """
        self.client = client

    async def get_order_manifest(self, store_id: int) -> Dict[str, Any]:
        """Get order manifest for a store."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/orders/manifest"
        )

    async def get_order_details(self, store_id: int, order_id: int) -> Dict[str, Any]:
        """Get order details."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/orders/{order_id}"
        )

    async def get_order_feedback(self, store_id: int, order_id: int) -> Dict[str, Any]:
        """Get order feedback."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/orders/{order_id}/feedback"
        )

    async def search_orders(
        self, store_id: int, search_criteria: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search orders with criteria."""
        if search_criteria is None:
            search_criteria = {}
        return await self.client._make_api_request(
            f"/stores/{store_id}/orders/search", method="POST", data=search_criteria
        )

    async def get_order_items(self, store_id: int, order_id: int) -> Dict[str, Any]:
        """Get order items."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/orders/{order_id}/items"
        )

    async def get_order_tracking_numbers(
        self, store_id: int, order_id: int
    ) -> Dict[str, Any]:
        """Get order tracking numbers."""
        return await self.client._make_api_request(
            f"/stores/{store_id}/orders/{order_id}/tracking"
        )

    async def add_order_tracking_number(
        self,
        store_id: int,
        order_id: int,
        tracking_number: str,
        carrier: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add tracking number to an order."""
        data = {"trackingNumber": tracking_number}
        if carrier:
            data["carrier"] = carrier
        return await self.client._make_api_request(
            f"/stores/{store_id}/orders/{order_id}/tracking", method="POST", data=data
        )
