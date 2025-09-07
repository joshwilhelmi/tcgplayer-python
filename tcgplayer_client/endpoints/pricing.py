"""
Pricing endpoints for TCGplayer API.

This module contains market and buylist pricing operations:
- Market prices for products, SKUs, and groups
- Buylist prices for products, SKUs, and groups
- Individual product condition pricing
"""

from typing import Any, Dict, List, Union

from ..client import TCGplayerClient


class PricingEndpoints:
    """Market and buylist pricing API endpoints."""

    def __init__(self, client: TCGplayerClient):
        """
        Initialize pricing endpoints.

        Args:
            client: TCGplayer client instance
        """
        self.client = client

    async def get_market_price_by_sku(
        self, product_condition_id: int
    ) -> Dict[str, Any]:
        """
        Get the current market price for a specific SKU (product condition).

        Args:
            product_condition_id: The product condition ID (SKU) to get market price for

        Returns:
            Dict containing market price information with price ranges
        """
        return await self.client._make_api_request(
            f"/pricing/marketprices/{product_condition_id}"
        )

    async def get_product_market_prices(
        self, product_ids: Union[List[int], str]
    ) -> Dict[str, Any]:
        """
        Get market prices for one or more products.

        Args:
            product_ids: List of product IDs or comma-separated string of product IDs

        Returns:
            Dict containing market price information for all requested products
        """
        if isinstance(product_ids, list):
            product_ids_str = ",".join(map(str, product_ids))
        else:
            product_ids_str = product_ids

        return await self.client._make_api_request(
            f"/pricing/product/{product_ids_str}"
        )

    async def get_sku_market_prices(
        self, sku_ids: Union[List[int], str]
    ) -> Dict[str, Any]:
        """
        Get market prices for one or more SKUs (product conditions).

        Args:
            sku_ids: List of SKU IDs or comma-separated string of SKU IDs

        Returns:
            Dict containing market price information for all requested SKUs
        """
        if isinstance(sku_ids, list):
            sku_ids_str = ",".join(map(str, sku_ids))
        else:
            sku_ids_str = sku_ids

        return await self.client._make_api_request(f"/pricing/sku/{sku_ids_str}")

    async def get_group_market_prices(self, group_id: int) -> Dict[str, Any]:
        """
        Get market prices for all products in a specific group/set.

        Args:
            group_id: The ID of the product group/set to get pricing for

        Returns:
            Dict containing market price information for all products in the group
        """
        return await self.client._make_api_request(f"/pricing/group/{group_id}")

    async def get_product_buylist_prices(
        self, product_ids: Union[List[int], str]
    ) -> Dict[str, Any]:
        """
        Get buylist prices for one or more products.

        Args:
            product_ids: List of product IDs or comma-separated string of product IDs

        Returns:
            Dict containing buylist price information for all requested products
        """
        if isinstance(product_ids, list):
            product_ids_str = ",".join(map(str, product_ids))
        else:
            product_ids_str = product_ids

        return await self.client._make_api_request(
            f"/pricing/buy/product/{product_ids_str}"
        )

    async def get_sku_buylist_prices(
        self, sku_ids: Union[List[int], str]
    ) -> Dict[str, Any]:
        """
        Get buylist prices for one or more SKUs.

        Args:
            sku_ids: List of SKU IDs or comma-separated string of SKU IDs

        Returns:
            Dict containing buylist price information for all requested SKUs
        """
        if isinstance(sku_ids, list):
            sku_ids_str = ",".join(map(str, sku_ids))
        else:
            sku_ids_str = sku_ids

        return await self.client._make_api_request(f"/pricing/buy/sku/{sku_ids_str}")

    async def get_group_buylist_prices(self, group_id: int) -> Dict[str, Any]:
        """
        Get buylist prices for all products in a specific group/set.

        Args:
            group_id: The ID of the product group/set to get buylist pricing for

        Returns:
            Dict containing buylist price information for all products in the group
        """
        return await self.client._make_api_request(f"/pricing/buy/group/{group_id}")
