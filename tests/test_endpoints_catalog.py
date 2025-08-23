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

    @pytest.mark.asyncio
    async def test_get_categories(self):
        """Test getting all categories."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_categories()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/categories")

    @pytest.mark.asyncio
    async def test_get_category_details(self):
        """Test getting category details."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_category_details(123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/categories/123")

    @pytest.mark.asyncio
    async def test_get_group_details(self):
        """Test getting group details."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_group_details(456)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/groups/456")

    @pytest.mark.asyncio
    async def test_get_condition_names(self):
        """Test getting condition names."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_condition_names()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/conditions")

    @pytest.mark.asyncio
    async def test_get_language_names(self):
        """Test getting language names."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_language_names()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/languages")

    @pytest.mark.asyncio
    async def test_get_rarities(self):
        """Test getting rarities."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_rarities()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/rarities")

    @pytest.mark.asyncio
    async def test_get_skus(self):
        """Test getting SKUs for products."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        product_ids = [1, 2, 3]
        result = await catalog.get_skus(product_ids)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/1,2,3/skus"
        )

    @pytest.mark.asyncio
    async def test_get_sku_details(self):
        """Test getting SKU details."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        sku_ids = [10, 20, 30]
        result = await catalog.get_sku_details(sku_ids)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/catalog/skus/10,20,30")

    @pytest.mark.asyncio
    async def test_get_products_no_filters(self):
        """Test getting products with no filters."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_products()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products", params={}
        )

    @pytest.mark.asyncio
    async def test_get_products_with_category_filter(self):
        """Test getting products with category filter."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_products(category_id=123)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products", params={"categoryId": 123}
        )

    @pytest.mark.asyncio
    async def test_get_products_with_multiple_filters(self):
        """Test getting products with multiple filters."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_products(
            category_id=123,
            group_id=456,
            product_name="Test Product",
            limit=10,
            offset=20,
        )

        expected_params = {
            "categoryId": 123,
            "groupId": 456,
            "productName": "Test Product",
            "limit": 10,
            "offset": 20,
        }

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products", params=expected_params
        )

    @pytest.mark.asyncio
    async def test_get_product_details(self):
        """Test getting product details."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        product_ids = [100, 200, 300]
        result = await catalog.get_product_details(product_ids)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/100,200,300"
        )

    @pytest.mark.asyncio
    async def test_get_product_media_single_product(self):
        """Test getting product media for single product."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        product_ids = [500]
        result = await catalog.get_product_media(product_ids)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/500/media"
        )

    @pytest.mark.asyncio
    async def test_get_product_media_multiple_products(self):
        """Test getting product media for multiple products (uses first product)."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        product_ids = [500, 600, 700]
        result = await catalog.get_product_media(product_ids)

        assert result == {"success": True, "results": []}
        # Should use the first product ID
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/500/media"
        )

    @pytest.mark.asyncio
    async def test_get_product_by_gtin(self):
        """Test getting product by GTIN."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        gtin = "1234567890123"
        result = await catalog.get_product_by_gtin(gtin)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            f"/catalog/products/gtin/{gtin}"
        )

    @pytest.mark.asyncio
    async def test_get_related_products(self):
        """Test getting related products."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        product_ids = [800, 900]
        result = await catalog.get_related_products(product_ids)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products/800,900/related"
        )

    @pytest.mark.asyncio
    async def test_get_products_by_name(self):
        """Test getting products by name."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        product_name = "Black Lotus"
        result = await catalog.get_products(product_name=product_name)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products", params={"productName": "Black Lotus"}
        )

    @pytest.mark.asyncio
    async def test_get_products_with_pagination(self):
        """Test getting products with pagination."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        catalog = CatalogEndpoints(mock_client)
        result = await catalog.get_products(limit=50, offset=100)

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with(
            "/catalog/products", params={"limit": 50, "offset": 100}
        )

    def test_catalog_endpoints_repr(self):
        """Test catalog endpoints string representation."""
        mock_client = MagicMock()
        catalog = CatalogEndpoints(mock_client)
        repr_str = repr(catalog)

        # Note: The current implementation doesn't customize repr
        # This test verifies the basic object representation
        assert "CatalogEndpoints" in repr_str
