"""
Catalog endpoints for TCGPlayer API.

This module contains all catalog-related operations including:
- Categories and groups
- Products and SKUs
- Media and search functionality
"""

from typing import Any, Dict, List, Optional

from ..client import TCGPlayerClient
from ..validation import (
    validate_id,
    validate_non_negative_integer,
    validate_positive_integer,
)


class CatalogEndpoints:
    """Catalog-related API endpoints."""

    def __init__(self, client: TCGPlayerClient):
        """
        Initialize catalog endpoints.

        Args:
            client: TCGPlayer client instance
        """
        self.client = client

    async def get_categories(self) -> Dict[str, Any]:
        """Get all product categories."""
        return await self.client._make_api_request("/catalog/categories")

    async def get_category_details(self, category_id: int) -> Dict[str, Any]:
        """Get details for a specific category."""
        category_id = validate_id(category_id, "category_id")
        return await self.client._make_api_request(f"/catalog/categories/{category_id}")

    async def get_group_details(self, group_id: int) -> Dict[str, Any]:
        """Get details for a specific group."""
        group_id = validate_id(group_id, "group_id")
        return await self.client._make_api_request(f"/catalog/groups/{group_id}")

    async def get_condition_names(self) -> Dict[str, Any]:
        """Get all condition names."""
        return await self.client._make_api_request("/catalog/conditions")

    async def get_language_names(self) -> Dict[str, Any]:
        """Get all language names."""
        return await self.client._make_api_request("/catalog/languages")

    async def get_rarities(self) -> Dict[str, Any]:
        """Get all rarities."""
        return await self.client._make_api_request("/catalog/rarities")

    async def get_skus(self, product_ids: List[int]) -> Dict[str, Any]:
        """Get SKUs for products."""
        return await self.client._make_api_request(
            f"/catalog/products/{','.join(map(str, product_ids))}/skus"
        )

    async def get_sku_details(self, sku_ids: List[int]) -> Dict[str, Any]:
        """Get details for specific SKUs."""
        return await self.client._make_api_request(
            f"/catalog/skus/{','.join(map(str, sku_ids))}"
        )

    async def get_products(
        self,
        category_id: Optional[int] = None,
        group_id: Optional[int] = None,
        product_name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get products with various filters."""
        params: Dict[str, Any] = {}
        if category_id is not None:
            params["categoryId"] = category_id
        if group_id is not None:
            params["groupId"] = group_id
        if product_name is not None:
            params["productName"] = product_name
        if limit is not None:
            params["limit"] = validate_positive_integer(limit, "limit")
        if offset is not None:
            params["offset"] = validate_non_negative_integer(offset, "offset")

        return await self.client._make_api_request("/catalog/products", params=params)

    async def get_product_details(self, product_ids: List[int]) -> Dict[str, Any]:
        """Get detailed information for specific products."""
        return await self.client._make_api_request(
            f"/catalog/products/{','.join(map(str, product_ids))}"
        )

    async def get_product_media(self, product_ids: List[int]) -> Dict[str, Any]:
        """Get media (images) for products."""
        # For now, use the first product ID as per original implementation
        if len(product_ids) == 1:
            return await self.client._make_api_request(
                f"/catalog/products/{product_ids[0]}/media"
            )
        else:
            # For multiple products, return the first product's media
            return await self.client._make_api_request(
                f"/catalog/products/{product_ids[0]}/media"
            )

    async def get_product_by_gtin(self, gtin: str) -> Dict[str, Any]:
        """Get product details by GTIN."""
        return await self.client._make_api_request(f"/catalog/products/gtin/{gtin}")

    async def get_related_products(self, product_ids: List[int]) -> Dict[str, Any]:
        """Get related products for specific products."""
        return await self.client._make_api_request(
            f"/catalog/products/{','.join(map(str, product_ids))}/related"
        )

    async def get_category_media(self, category_id: int) -> Dict[str, Any]:
        """Get media for a specific category."""
        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/media"
        )

    async def get_category_search_manifest(self, category_id: int) -> Dict[str, Any]:
        """Get category search manifest for advanced search functionality."""
        return await self.client._make_api_request(
            f"/v1.39.0/catalog/categories/{category_id}/search/manifest"
        )

    async def search_category_products(
        self, category_id: int, search_criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Search for products within a specific category using advanced search
        criteria."""
        return await self.client._make_api_request(
            f"/v1.39.0/catalog/categories/{category_id}/search",
            method="POST",
            data=search_criteria,
        )
