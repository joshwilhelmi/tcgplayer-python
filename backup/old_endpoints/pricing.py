"""
Pricing endpoints for TCGPlayer API.

This module contains all pricing-related operations including:
- Market prices (buylist functionality discontinued by TCGPlayer)
- Group-based pricing
- SKU-specific pricing
"""

from typing import Any, Dict, List

from ..client import TCGPlayerClient


class PricingEndpoints:
    """Pricing-related API endpoints."""

    def __init__(self, client: TCGPlayerClient):
        """
        Initialize pricing endpoints.

        Args:
            client: TCGPlayer client instance
        """
        self.client = client

    async def get_product_prices(self, product_ids: List[int]) -> Dict[str, Any]:
        """Get pricing information for products."""
        params = {"productIds": ",".join(map(str, product_ids))}
        return await self.client._make_api_request("/pricing/product", params=params)

    async def get_market_prices(self, product_ids: List[int]) -> Dict[str, Any]:
        """Get market prices for products."""
        # Use the correct endpoint from API documentation: /pricing/product/{productIds}
        product_ids_str = ",".join(map(str, product_ids))
        return await self.client._make_api_request(
            f"/pricing/product/{product_ids_str}"
        )

    # Buylist functionality discontinued by TCGPlayer
    # async def get_buylist_prices(self, product_ids: List[int]) -> Dict[str, Any]:
    #     """Get buylist prices for products."""
    #     params = {"productIds": ",".join(map(str, product_ids))}
    #     return await self.client._make_api_request(
    #         "/pricing/buy/products", params=params
    #     )

    async def get_sku_market_prices(self, sku_ids: List[int]) -> Dict[str, Any]:
        """Get market prices for specific SKUs."""
        # Use the correct endpoint from API documentation: /pricing/marketprices/skus
        params = {"skuIds": ",".join(map(str, sku_ids))}
        return await self.client._make_api_request(
            "/pricing/marketprices/skus", params=params
        )

    # Buylist functionality discontinued by TCGPlayer
    # async def get_sku_buylist_prices(self, sku_ids: List[int]) -> Dict[str, Any]:
    #     """Get buylist prices for specific SKUs."""
    #     params = {"skuIds": ",".join(map(str, sku_ids))}
    #     return await self.client._make_api_request("/pricing/buy/skus", params=params)

    async def get_market_price_by_sku(
        self, product_condition_id: int
    ) -> Dict[str, Any]:
        """Get market price by product condition ID."""
        return await self.client._make_api_request(
            f"/pricing/marketprices/{product_condition_id}"
        )

    async def get_product_prices_by_group(self, group_id: int) -> Dict[str, Any]:
        """Get product prices by group ID."""
        return await self.client._make_api_request(f"/pricing/group/{group_id}")

    # Buylist functionality discontinued by TCGPlayer
    # async def get_product_buylist_prices_by_group(
    #     self, group_id: int
    #     ) -> Dict[str, Any]:
    #     """Get product buylist prices by group ID."""
    #     return await self.client._make_api_request(f"/pricing/buy/group/{group_id}")
