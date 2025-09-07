"""
Unit tests for the catalog endpoints module.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from tcgplayer_client.endpoints.catalog import CatalogEndpoints


class TestCatalogEndpoints:
    """Test cases for CatalogEndpoints class."""

    def test_catalog_endpoints_initialization(self):
        """Test catalog endpoints initialization."""
        mock_client = MagicMock()
        catalog = CatalogEndpoints(mock_client)

        assert catalog.client is mock_client

    # Category endpoints tests
    @pytest.mark.asyncio
    async def test_list_all_categories(self):
        """Test listing all categories with pagination."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_categories(
            offset=10, limit=20, sort_order="name", sort_desc=True
        )

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories",
            params={"offset": 10, "limit": 20, "sortOrder": "name", "sortDesc": True},
        )

    @pytest.mark.asyncio
    async def test_get_category_details_single(self):
        """Test getting category details for single category."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_category_details(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/categories/123")

    @pytest.mark.asyncio
    async def test_get_category_details_multiple(self):
        """Test getting category details for multiple categories."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_category_details([123, 456, 789])

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123,456,789"
        )

    @pytest.mark.asyncio
    async def test_get_category_search_manifest(self):
        """Test getting category search manifest."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_category_search_manifest(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/search/manifest"
        )

    @pytest.mark.asyncio
    async def test_search_category_products(self):
        """Test searching products within category."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        search_criteria = {"sort": "name", "limit": 10, "filters": []}
        result = await catalog.search_category_products(123, search_criteria)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/search", method="POST", data=search_criteria
        )

    @pytest.mark.asyncio
    async def test_list_all_category_groups(self):
        """Test listing groups for category."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_category_groups(123, offset=5, limit=15)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/groups", params={"offset": 5, "limit": 15}
        )

    @pytest.mark.asyncio
    async def test_list_all_category_rarities(self):
        """Test listing rarities for category."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_category_rarities(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/rarities"
        )

    @pytest.mark.asyncio
    async def test_list_all_category_printings(self):
        """Test listing printings for category."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_category_printings(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/printings"
        )

    @pytest.mark.asyncio
    async def test_list_all_category_conditions(self):
        """Test listing conditions for category."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_category_conditions(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/conditions"
        )

    @pytest.mark.asyncio
    async def test_list_all_category_languages(self):
        """Test listing languages for category."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_category_languages(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/languages"
        )

    @pytest.mark.asyncio
    async def test_list_all_category_media(self):
        """Test listing media for category."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_category_media(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/media"
        )

    # Group endpoints tests
    @pytest.mark.asyncio
    async def test_list_all_groups_details(self):
        """Test listing all groups with details."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_groups_details(
            offset=10, limit=20, category_id=123
        )

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/groups", params={"offset": 10, "limit": 20, "categoryId": 123}
        )

    @pytest.mark.asyncio
    async def test_get_group_details_single(self):
        """Test getting group details for single group."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_group_details(456)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/groups/456")

    @pytest.mark.asyncio
    async def test_get_group_details_multiple(self):
        """Test getting group details for multiple groups."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_group_details([456, 789, 101])

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/groups/456,789,101"
        )

    @pytest.mark.asyncio
    async def test_list_all_group_media(self):
        """Test listing media for group."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_group_media(456)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/groups/456/media"
        )

    # Product endpoints tests
    @pytest.mark.asyncio
    async def test_get_product_details_single(self):
        """Test getting product details for single product."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_product_details(789)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/products/789")

    @pytest.mark.asyncio
    async def test_get_product_details_multiple(self):
        """Test getting product details for multiple products."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_product_details([100, 200, 300])

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/100,200,300"
        )

    @pytest.mark.asyncio
    async def test_get_product_details_by_gtin(self):
        """Test getting product details by GTIN."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_product_details_by_gtin("1234567890123")

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/gtin/1234567890123"
        )

    @pytest.mark.asyncio
    async def test_get_product_details_by_gtin_invalid(self):
        """Test getting product details by invalid GTIN."""
        mock_client = MagicMock()
        catalog = CatalogEndpoints(mock_client)

        with pytest.raises(ValueError, match="GTIN must be a non-empty string"):
            await catalog.get_product_details_by_gtin("")

        with pytest.raises(ValueError, match="GTIN must be a non-empty string"):
            await catalog.get_product_details_by_gtin(None)

    @pytest.mark.asyncio
    async def test_list_product_skus(self):
        """Test listing SKUs for product."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_product_skus(789)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/789/skus"
        )

    @pytest.mark.asyncio
    async def test_list_related_products(self):
        """Test listing related products."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_related_products(789)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/789/productsalsopurchased"
        )

    @pytest.mark.asyncio
    async def test_list_all_product_media_types(self):
        """Test listing media for product."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_product_media_types(789)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/789/media"
        )

    @pytest.mark.asyncio
    async def test_list_all_products(self):
        """Test listing all products with filters."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_all_products(
            category_id=123, product_types="Cards", limit=50
        )

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products",
            params={"categoryId": 123, "productTypes": "Cards", "limit": 50},
        )

    # Conditions endpoints tests
    @pytest.mark.asyncio
    async def test_list_conditions(self):
        """Test listing all conditions."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.list_conditions()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/conditions")

    # SKU endpoints tests
    @pytest.mark.asyncio
    async def test_get_sku_details_single(self):
        """Test getting SKU details for single SKU."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_sku_details(999)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/skus/999")

    @pytest.mark.asyncio
    async def test_get_sku_details_multiple(self):
        """Test getting SKU details for multiple SKUs."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_sku_details([10, 20, 30])

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/skus/10,20,30")

    # Legacy method tests for backward compatibility
    @pytest.mark.asyncio
    async def test_get_categories_legacy(self):
        """Test legacy get_categories method."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_categories()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories", params={}
        )

    @pytest.mark.asyncio
    async def test_get_condition_names_legacy(self):
        """Test legacy get_condition_names method."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_condition_names()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/conditions")

    @pytest.mark.asyncio
    async def test_get_products_legacy(self):
        """Test legacy get_products method."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_products(category_id=123, limit=10)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products", params={"categoryId": 123, "limit": 10}
        )

    @pytest.mark.asyncio
    async def test_get_product_media_legacy_single(self):
        """Test legacy get_product_media method with single product."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_product_media(500)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/500/media"
        )

    @pytest.mark.asyncio
    async def test_get_product_media_legacy_list(self):
        """Test legacy get_product_media method with list."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_product_media([500, 600])

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/500/media"
        )

    @pytest.mark.asyncio
    async def test_get_product_media_legacy_invalid(self):
        """Test legacy get_product_media method with invalid input."""
        mock_client = MagicMock()
        catalog = CatalogEndpoints(mock_client)

        with pytest.raises(
            ValueError, match="product_ids must be an integer or non-empty list"
        ):
            await catalog.get_product_media([])

    @pytest.mark.asyncio
    async def test_get_product_by_gtin_legacy(self):
        """Test legacy get_product_by_gtin method."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_product_by_gtin("1234567890123")

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/gtin/1234567890123"
        )

    @pytest.mark.asyncio
    async def test_get_related_products_legacy_single(self):
        """Test legacy get_related_products method with single product."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_related_products(800)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/800/productsalsopurchased"
        )

    @pytest.mark.asyncio
    async def test_get_related_products_legacy_list(self):
        """Test legacy get_related_products method with list."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_related_products([800, 900])

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/800/productsalsopurchased"
        )

    @pytest.mark.asyncio
    async def test_get_category_media_legacy(self):
        """Test legacy get_category_media method."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_category_media(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/categories/123/media"
        )

    @pytest.mark.asyncio
    async def test_get_skus_legacy_single(self):
        """Test legacy get_skus method with single product."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_skus(100)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/100/skus"
        )

    @pytest.mark.asyncio
    async def test_get_skus_legacy_list(self):
        """Test legacy get_skus method with list."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_skus([100, 200])

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/100/skus"
        )

    @pytest.mark.asyncio
    async def test_get_sku_details_legacy(self):
        """Test legacy get_sku_details method."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_sku_details_legacy([10, 20, 30])

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/skus/10,20,30")

    def test_catalog_endpoints_repr(self):
        """Test catalog endpoints string representation."""
        mock_client = MagicMock()
        catalog = CatalogEndpoints(mock_client)
        repr_str = repr(catalog)

        assert "CatalogEndpoints" in repr_str
