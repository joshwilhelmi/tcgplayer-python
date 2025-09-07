"""
Tests for Pricing endpoints.
"""

from unittest.mock import AsyncMock, Mock

import pytest

from tcgplayer_client.endpoints.pricing import PricingEndpoints
from tcgplayer_client.exceptions import APIError


class TestPricingEndpoints:
    """Test suite for Pricing endpoints."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_client._make_api_request = AsyncMock()
        self.pricing_endpoints = PricingEndpoints(self.mock_client)

    # Test get_market_price_by_sku
    @pytest.mark.asyncio
    async def test_get_market_price_by_sku_success(self):
        """Test successful market price retrieval by SKU."""
        # Arrange
        product_condition_id = 123456
        expected_response = {
            "success": True,
            "results": [
                {
                    "productConditionId": 123456,
                    "price": 15.99,
                    "lowestRange": 12.00,
                    "highestRange": 20.00,
                }
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_market_price_by_sku(
            product_condition_id
        )

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            f"/pricing/marketprices/{product_condition_id}"
        )

    @pytest.mark.asyncio
    async def test_get_market_price_by_sku_not_found(self):
        """Test market price retrieval by SKU when not found."""
        # Arrange
        product_condition_id = 99999
        self.mock_client._make_api_request.side_effect = APIError(
            "Market price not found", status_code=404
        )

        # Act & Assert
        with pytest.raises(APIError) as exc_info:
            await self.pricing_endpoints.get_market_price_by_sku(product_condition_id)

        assert exc_info.value.status_code == 404

    # Test get_product_market_prices
    @pytest.mark.asyncio
    async def test_get_product_market_prices_with_list(self):
        """Test product market prices with list of IDs."""
        # Arrange
        product_ids = [123, 456, 789]
        expected_response = {
            "success": True,
            "results": [
                {
                    "productId": 123,
                    "lowPrice": 10.00,
                    "midPrice": 15.00,
                    "highPrice": 20.00,
                    "marketPrice": 15.99,
                    "directLowPrice": 12.00,
                    "subTypeName": "Cards",
                },
                {
                    "productId": 456,
                    "lowPrice": 5.00,
                    "midPrice": 8.00,
                    "highPrice": 12.00,
                    "marketPrice": 8.99,
                    "directLowPrice": 6.00,
                    "subTypeName": "Cards",
                },
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_product_market_prices(product_ids)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/pricing/product/123,456,789"
        )

    @pytest.mark.asyncio
    async def test_get_product_market_prices_with_string(self):
        """Test product market prices with comma-separated string."""
        # Arrange
        product_ids = "123,456,789"
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_product_market_prices(product_ids)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/pricing/product/123,456,789"
        )

    @pytest.mark.asyncio
    async def test_get_product_market_prices_single_id(self):
        """Test product market prices with single ID in list."""
        # Arrange
        product_ids = [123]
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_product_market_prices(product_ids)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/pricing/product/123"
        )

    # Test get_sku_market_prices
    @pytest.mark.asyncio
    async def test_get_sku_market_prices_success(self):
        """Test successful SKU market prices retrieval."""
        # Arrange
        sku_ids = [111, 222, 333]
        expected_response = {
            "success": True,
            "results": [
                {
                    "skuId": 111,
                    "lowPrice": 10.00,
                    "lowestShipping": 1.50,
                    "lowestListingPrice": 11.50,
                    "marketPrice": 12.99,
                    "directLowPrice": 11.00,
                }
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_sku_market_prices(sku_ids)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/pricing/sku/111,222,333"
        )

    @pytest.mark.asyncio
    async def test_get_sku_market_prices_with_string(self):
        """Test SKU market prices with string input."""
        # Arrange
        sku_ids = "111,222,333"
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_sku_market_prices(sku_ids)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/pricing/sku/111,222,333"
        )

    # Test get_group_market_prices
    @pytest.mark.asyncio
    async def test_get_group_market_prices_success(self):
        """Test successful group market prices retrieval."""
        # Arrange
        group_id = 789
        expected_response = {
            "success": True,
            "results": [
                {
                    "productId": 123,
                    "lowPrice": 8.00,
                    "midPrice": 12.00,
                    "highPrice": 18.00,
                    "marketPrice": 13.99,
                    "directLowPrice": 10.00,
                    "subTypeName": "Cards",
                }
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_group_market_prices(group_id)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            f"/pricing/group/{group_id}"
        )

    # Test get_product_buylist_prices
    @pytest.mark.asyncio
    async def test_get_product_buylist_prices_success(self):
        """Test successful product buylist prices retrieval."""
        # Arrange
        product_ids = [123, 456]
        expected_response = {
            "success": True,
            "results": [
                {
                    "productId": 123,
                    "prices": {"high": 12.00, "market": 10.00},
                    "skus": [
                        {"skuId": 111, "prices": {"high": 12.00, "market": 10.00}}
                    ],
                }
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_product_buylist_prices(product_ids)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/pricing/buy/product/123,456"
        )

    @pytest.mark.asyncio
    async def test_get_product_buylist_prices_with_string(self):
        """Test product buylist prices with string input."""
        # Arrange
        product_ids = "123,456"
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_product_buylist_prices(product_ids)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/pricing/buy/product/123,456"
        )

    # Test get_sku_buylist_prices
    @pytest.mark.asyncio
    async def test_get_sku_buylist_prices_success(self):
        """Test successful SKU buylist prices retrieval."""
        # Arrange
        sku_ids = [111, 222]
        expected_response = {
            "success": True,
            "results": [
                {"skuId": 111, "prices": {"high": 8.00, "market": 6.50}},
                {"skuId": 222, "prices": {"high": 15.00, "market": 12.00}},
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_sku_buylist_prices(sku_ids)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/pricing/buy/sku/111,222"
        )

    # Test get_group_buylist_prices
    @pytest.mark.asyncio
    async def test_get_group_buylist_prices_success(self):
        """Test successful group buylist prices retrieval."""
        # Arrange
        group_id = 456
        expected_response = {
            "success": True,
            "results": [{"productId": 123, "prices": {"high": 20.00, "market": 18.00}}],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_group_buylist_prices(group_id)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            f"/pricing/buy/group/{group_id}"
        )

    # Test error handling scenarios
    @pytest.mark.asyncio
    async def test_api_error_handling(self):
        """Test proper API error handling."""
        # Arrange
        product_condition_id = 123
        self.mock_client._make_api_request.side_effect = APIError(
            "API Error occurred", status_code=500
        )

        # Act & Assert
        with pytest.raises(APIError) as exc_info:
            await self.pricing_endpoints.get_market_price_by_sku(product_condition_id)

        assert exc_info.value.status_code == 500
        assert "API Error occurred" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_empty_results(self):
        """Test handling of empty results."""
        # Arrange
        product_ids = [999]
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.pricing_endpoints.get_product_market_prices(product_ids)

        # Assert
        assert result == expected_response
        assert len(result["results"]) == 0

    # Test initialization and methods existence
    def test_pricing_endpoints_initialization(self):
        """Test PricingEndpoints initialization."""
        # Test that client is properly stored
        assert self.pricing_endpoints.client == self.mock_client

        # Test that all expected methods exist
        expected_methods = [
            "get_market_price_by_sku",
            "get_product_market_prices",
            "get_sku_market_prices",
            "get_group_market_prices",
            "get_product_buylist_prices",
            "get_sku_buylist_prices",
            "get_group_buylist_prices",
        ]

        for method_name in expected_methods:
            assert hasattr(self.pricing_endpoints, method_name)
            assert callable(getattr(self.pricing_endpoints, method_name))

    @pytest.mark.asyncio
    async def test_correct_api_paths_used(self):
        """Test that correct API paths are used (addressing previous issues)."""
        # This test ensures we're using the correct paths as defined in API docs

        # Test market price by SKU path
        await self.pricing_endpoints.get_market_price_by_sku(123)
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/pricing/marketprices/123"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test product market prices path
        await self.pricing_endpoints.get_product_market_prices([123, 456])
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/pricing/product/123,456"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test SKU market prices path (corrected from old wrong path)
        await self.pricing_endpoints.get_sku_market_prices([111, 222])
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/pricing/sku/111,222"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test group market prices path
        await self.pricing_endpoints.get_group_market_prices(789)
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/pricing/group/789"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test product buylist prices path (restored endpoint)
        await self.pricing_endpoints.get_product_buylist_prices([123])
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/pricing/buy/product/123"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test SKU buylist prices path (restored endpoint)
        await self.pricing_endpoints.get_sku_buylist_prices([111])
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/pricing/buy/sku/111"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test group buylist prices path (restored endpoint)
        await self.pricing_endpoints.get_group_buylist_prices(456)
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/pricing/buy/group/456"

    @pytest.mark.asyncio
    async def test_parameter_flexibility(self):
        """Test that endpoints handle both list and string parameters correctly."""
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # Test with list
        await self.pricing_endpoints.get_product_market_prices([123, 456])
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[-1][0][0] == "/pricing/product/123,456"

        # Test with string
        await self.pricing_endpoints.get_product_market_prices("789,101")
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[-1][0][0] == "/pricing/product/789,101"

        # Test SKU endpoints similarly
        await self.pricing_endpoints.get_sku_market_prices([111, 222])
        await self.pricing_endpoints.get_sku_market_prices("333,444")

        calls = self.mock_client._make_api_request.call_args_list
        assert "/pricing/sku/111,222" in [call[0][0] for call in calls]
        assert "/pricing/sku/333,444" in [call[0][0] for call in calls]
