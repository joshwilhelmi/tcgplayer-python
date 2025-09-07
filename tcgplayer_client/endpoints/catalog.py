"""
Catalog endpoints for TCGplayer API.

This module contains all catalog-related operations including:
- Categories and groups
- Products and SKUs
- Media and search functionality
"""

from typing import Any, Dict, List, Optional, Union

from ..client import TCGplayerClient
from ..validation import (
    validate_id,
    validate_non_negative_integer,
    validate_positive_integer,
)


class CatalogEndpoints:
    """Catalog-related API endpoints."""

    def __init__(self, client: TCGplayerClient):
        """
        Initialize catalog endpoints.

        Args:
            client: TCGplayer client instance
        """
        self.client = client

    # Categories
    async def list_all_categories(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort_order: Optional[str] = None,
        sort_desc: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        List all categories supported by TCGplayer.

        Args:
            offset: Number of categories to skip (default: 0)
            limit: Maximum number of categories to return (default: 10)
            sort_order: Property to sort by (default: name)
            sort_desc: If true, sort descending (default: false)

        Returns:
            Paginated list of all categories
        """
        params: Dict[str, Any] = {}
        if offset is not None:
            params["offset"] = validate_non_negative_integer(offset, "offset")
        if limit is not None:
            params["limit"] = validate_positive_integer(limit, "limit")
        if sort_order is not None:
            params["sortOrder"] = sort_order
        if sort_desc is not None:
            params["sortDesc"] = sort_desc

        return await self.client._make_api_request("/catalog/categories", params=params)

    async def get_category_details(
        self, category_ids: Union[int, List[int]]
    ) -> Dict[str, Any]:
        """
        Get category details for specified category IDs.

        Args:
            category_ids: Single category ID or list of category IDs

        Returns:
            Array of categories with detailed information
        """
        if isinstance(category_ids, int):
            category_ids = [category_ids]

        for cat_id in category_ids:
            validate_id(cat_id, "category_id")

        ids_str = ",".join(map(str, category_ids))
        return await self.client._make_api_request(f"/catalog/categories/{ids_str}")

    async def get_category_search_manifest(self, category_id: int) -> Dict[str, Any]:
        """
        Get search manifest for a category describing sorting options and filters.

        Args:
            category_id: The ID of the category to get search manifest for

        Returns:
            Search manifest with sorting and filter options
        """
        category_id = validate_id(category_id, "category_id")
        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/search/manifest"
        )

    async def search_category_products(
        self,
        category_id: int,
        search_criteria: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Search for products within a specific category using filters and sorting.

        Args:
            category_id: The ID of the category to search within
            search_criteria: Search criteria including sort, limit, offset, and filters

        Returns:
            Search results containing product IDs matching the criteria
        """
        category_id = validate_id(category_id, "category_id")
        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/search",
            method="POST",
            data=search_criteria,
        )

    async def list_all_category_groups(
        self,
        category_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all groups/sets for a specific category.

        Args:
            category_id: Category to retrieve groups for
            offset: Pagination start point
            limit: Number of results to return

        Returns:
            Paginated list of groups for the category
        """
        category_id = validate_id(category_id, "category_id")
        params: Dict[str, Any] = {}
        if offset is not None:
            params["offset"] = validate_non_negative_integer(offset, "offset")
        if limit is not None:
            params["limit"] = validate_positive_integer(limit, "limit")

        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/groups", params=params
        )

    async def list_all_category_rarities(self, category_id: int) -> Dict[str, Any]:
        """
        List all rarities for a specific category.

        Args:
            category_id: Category to retrieve rarities for

        Returns:
            Array of rarity objects for the category
        """
        category_id = validate_id(category_id, "category_id")
        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/rarities"
        )

    async def list_all_category_printings(self, category_id: int) -> Dict[str, Any]:
        """
        List all printing options for a specific category.

        Args:
            category_id: Category to retrieve printings for

        Returns:
            Array of printing options for the category
        """
        category_id = validate_id(category_id, "category_id")
        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/printings"
        )

    async def list_all_category_conditions(self, category_id: int) -> Dict[str, Any]:
        """
        List all available conditions for a specific category.

        Args:
            category_id: Category to retrieve conditions for

        Returns:
            Array of condition objects for the category
        """
        category_id = validate_id(category_id, "category_id")
        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/conditions"
        )

    async def list_all_category_languages(self, category_id: int) -> Dict[str, Any]:
        """
        List all available languages for a specific category.

        Args:
            category_id: Category to retrieve languages for

        Returns:
            Array of language objects for the category
        """
        category_id = validate_id(category_id, "category_id")
        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/languages"
        )

    async def list_all_category_media(self, category_id: int) -> Dict[str, Any]:
        """
        List all available media (images) for a specific category.

        Args:
            category_id: Category to retrieve media for

        Returns:
            Array of media objects for the category
        """
        category_id = validate_id(category_id, "category_id")
        return await self.client._make_api_request(
            f"/catalog/categories/{category_id}/media"
        )

    # Groups
    async def list_all_groups_details(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all product groups/sets with detailed information.

        Note: Despite API documentation marking categoryId as optional,
        the actual API requires it. If not provided, defaults to category 1 (Magic: The Gathering).

        Args:
            offset: Pagination start point
            limit: Number of results to return
            category_id: Filter groups by specific category (defaults to 1 if not provided)

        Returns:
            Paginated list of product groups with details
        """
        params: Dict[str, Any] = {}
        if offset is not None:
            params["offset"] = validate_non_negative_integer(offset, "offset")
        if limit is not None:
            params["limit"] = validate_positive_integer(limit, "limit")
        
        # API requires categoryId despite documentation saying it's optional
        # Default to category 1 (Magic: The Gathering) if not provided
        if category_id is None:
            category_id = 1
        params["categoryId"] = validate_id(category_id, "category_id")

        return await self.client._make_api_request("/catalog/groups", params=params)

    async def get_group_details(
        self, group_ids: Union[int, List[int]]
    ) -> Dict[str, Any]:
        """
        Get group details for specified group IDs.

        Args:
            group_ids: Single group ID or list of group IDs

        Returns:
            Array of group details
        """
        if isinstance(group_ids, int):
            group_ids = [group_ids]

        for group_id in group_ids:
            validate_id(group_id, "group_id")

        ids_str = ",".join(map(str, group_ids))
        return await self.client._make_api_request(f"/catalog/groups/{ids_str}")

    async def list_all_group_media(self, group_id: int) -> Dict[str, Any]:
        """
        List all available media (images) for a specific group.

        Args:
            group_id: Group to retrieve media for

        Returns:
            Array of media objects for the group
        """
        group_id = validate_id(group_id, "group_id")
        return await self.client._make_api_request(f"/catalog/groups/{group_id}/media")

    # Products
    async def get_product_details(
        self, product_ids: Union[int, List[int]]
    ) -> Dict[str, Any]:
        """
        Get product details for specified product IDs.

        Args:
            product_ids: Single product ID or list of product IDs

        Returns:
            Array of product details
        """
        if isinstance(product_ids, int):
            product_ids = [product_ids]

        for product_id in product_ids:
            validate_id(product_id, "product_id")

        ids_str = ",".join(map(str, product_ids))
        return await self.client._make_api_request(f"/catalog/products/{ids_str}")

    async def get_product_details_by_gtin(self, gtin: str) -> Dict[str, Any]:
        """
        Get product details using GTIN-13 product codes.

        Args:
            gtin: GTIN-13 product code

        Returns:
            Product details for the specified GTIN
        """
        if not gtin or not isinstance(gtin, str):
            raise ValueError("GTIN must be a non-empty string")

        return await self.client._make_api_request(f"/catalog/products/gtin/{gtin}")

    async def list_product_skus(self, product_id: int) -> Dict[str, Any]:
        """
        List SKUs for a specific product.

        Args:
            product_id: The product to retrieve SKUs for

        Returns:
            Array of SKU details for the product
        """
        product_id = validate_id(product_id, "product_id")
        return await self.client._make_api_request(
            f"/catalog/products/{product_id}/skus"
        )

    async def list_related_products(self, product_id: int) -> Dict[str, Any]:
        """
        List products commonly purchased with the specified product.

        Args:
            product_id: The product to find related products for

        Returns:
            Array of related products frequently bought together
        """
        product_id = validate_id(product_id, "product_id")
        return await self.client._make_api_request(
            f"/catalog/products/{product_id}/productsalsopurchased"
        )

    async def list_all_product_media_types(self, product_id: int) -> Dict[str, Any]:
        """
        List all media (primarily images) for a specific product.

        Args:
            product_id: Product to retrieve media for

        Returns:
            Array of media objects for the product
        """
        product_id = validate_id(product_id, "product_id")
        return await self.client._make_api_request(
            f"/catalog/products/{product_id}/media"
        )

    # Conditions
    async def list_conditions(self) -> Dict[str, Any]:
        """
        List all normalized conditions supported by TCGplayer.

        Returns:
            Array of all condition objects with IDs, names, and abbreviations
        """
        return await self.client._make_api_request("/catalog/conditions")

    # SKUs
    async def get_sku_details(self, sku_ids: Union[int, List[int]]) -> Dict[str, Any]:
        """
        Get SKU details for specified SKU IDs.

        Args:
            sku_ids: Single SKU ID or list of SKU IDs

        Returns:
            Array of SKU details
        """
        if isinstance(sku_ids, int):
            sku_ids = [sku_ids]

        for sku_id in sku_ids:
            validate_id(sku_id, "sku_id")

        ids_str = ",".join(map(str, sku_ids))
        return await self.client._make_api_request(f"/catalog/skus/{ids_str}")

    async def list_all_products(
        self,
        category_id: Optional[int] = None,
        product_types: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List all products with optional filters.

        Args:
            category_id: Filter products by category
            product_types: Filter by product type (e.g., "Cards")
            limit: Limit number of results returned

        Returns:
            Detailed product information based on search criteria
        """
        params: Dict[str, Any] = {}
        if category_id is not None:
            params["categoryId"] = validate_id(category_id, "category_id")
        if product_types is not None:
            params["productTypes"] = product_types
        if limit is not None:
            params["limit"] = validate_positive_integer(limit, "limit")

        return await self.client._make_api_request("/catalog/products", params=params)

    # Legacy method aliases for backward compatibility
    async def get_categories(self) -> Dict[str, Any]:
        """Get all product categories (legacy alias)."""
        return await self.list_all_categories()

    async def get_condition_names(self) -> Dict[str, Any]:
        """Get all condition names (legacy alias)."""
        return await self.list_conditions()

    async def get_products(
        self,
        category_id: Optional[int] = None,
        group_id: Optional[int] = None,
        product_name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get products with various filters (legacy alias)."""
        # Map old parameters to new endpoint
        return await self.list_all_products(category_id=category_id, limit=limit)

    async def get_product_media(
        self, product_ids: Union[int, List[int]]
    ) -> Dict[str, Any]:
        """Get media (images) for products (legacy alias)."""
        if isinstance(product_ids, list) and len(product_ids) > 0:
            return await self.list_all_product_media_types(product_ids[0])
        elif isinstance(product_ids, int):
            return await self.list_all_product_media_types(product_ids)
        else:
            raise ValueError(
                "product_ids must be an integer or non-empty list of integers"
            )

    async def get_product_by_gtin(self, gtin: str) -> Dict[str, Any]:
        """Get product details by GTIN (legacy alias)."""
        return await self.get_product_details_by_gtin(gtin)

    async def get_related_products(
        self, product_ids: Union[int, List[int]]
    ) -> Dict[str, Any]:
        """Get related products for specific products (legacy alias)."""
        if isinstance(product_ids, list) and len(product_ids) > 0:
            return await self.list_related_products(product_ids[0])
        elif isinstance(product_ids, int):
            return await self.list_related_products(product_ids)
        else:
            raise ValueError(
                "product_ids must be an integer or non-empty list of integers"
            )

    async def get_category_media(self, category_id: int) -> Dict[str, Any]:
        """Get media for a specific category (legacy alias)."""
        return await self.list_all_category_media(category_id)

    async def get_skus(self, product_ids: Union[int, List[int]]) -> Dict[str, Any]:
        """Get SKUs for products (legacy alias)."""
        if isinstance(product_ids, list) and len(product_ids) > 0:
            return await self.list_product_skus(product_ids[0])
        elif isinstance(product_ids, int):
            return await self.list_product_skus(product_ids)
        else:
            raise ValueError(
                "product_ids must be an integer or non-empty list of integers"
            )

    async def get_sku_details_legacy(self, sku_ids: List[int]) -> Dict[str, Any]:
        """Get details for specific SKUs (legacy alias)."""
        return await self.get_sku_details(sku_ids)
