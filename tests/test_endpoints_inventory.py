"""
Tests for Inventory endpoints.
"""

from unittest.mock import AsyncMock, Mock

import pytest

from tcgplayer_client.endpoints.inventory import InventoryEndpoints
from tcgplayer_client.exceptions import APIError


class TestInventoryEndpoints:
    """Test suite for Inventory endpoints."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_client._make_api_request = AsyncMock()
        self.inventory_endpoints = InventoryEndpoints(self.mock_client)

    # Test get_productlist_by_id
    @pytest.mark.asyncio
    async def test_get_productlist_by_id_success(self):
        """Test successful product list retrieval by ID."""
        # Arrange
        product_list_id = 12345
        expected_response = {
            "success": True,
            "results": [
                {
                    "productListItems": [
                        {
                            "productListItemId": 1,
                            "quantity": 2,
                            "productCondition": {
                                "productConditionId": 123,
                                "name": "Test Product",
                                "language": "English",
                                "isFoil": False,
                            },
                        }
                    ],
                    "productListId": 12345,
                    "productListKey": "test_key_12345",
                    "createdAt": "2023-01-01T12:00:00Z",
                }
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.inventory_endpoints.get_productlist_by_id(product_list_id)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            f"/inventory/productlists/{product_list_id}"
        )

    @pytest.mark.asyncio
    async def test_get_productlist_by_id_not_found(self):
        """Test product list retrieval by ID when not found."""
        # Arrange
        product_list_id = 99999
        self.mock_client._make_api_request.side_effect = APIError(
            "Product list not found", status_code=404
        )

        # Act & Assert
        with pytest.raises(APIError) as exc_info:
            await self.inventory_endpoints.get_productlist_by_id(product_list_id)

        assert exc_info.value.status_code == 404
        assert "not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_productlist_by_id_invalid_type(self):
        """Test product list retrieval with invalid ID type."""
        # Python will try to convert strings to ints in f-strings, so test behavior
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # This will actually work because f-string will convert to string
        result = await self.inventory_endpoints.get_productlist_by_id("123")
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_with(
            "/inventory/productlists/123"
        )

    # Test get_productlist_by_key
    @pytest.mark.asyncio
    async def test_get_productlist_by_key_success(self):
        """Test successful product list retrieval by key."""
        # Arrange
        product_list_key = "test_key_12345"
        expected_response = {
            "success": True,
            "results": [
                {
                    "productListItems": [
                        {
                            "productListItemId": 1,
                            "quantity": 1,
                            "productCondition": {
                                "productConditionId": 456,
                                "name": "Another Product",
                                "language": "English",
                                "isFoil": True,
                            },
                        }
                    ],
                    "productListId": 12345,
                    "productListKey": "test_key_12345",
                    "createdAt": "2023-01-01T12:00:00Z",
                }
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.inventory_endpoints.get_productlist_by_key(product_list_key)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            f"/inventory/productlists/{product_list_key}"
        )

    @pytest.mark.asyncio
    async def test_get_productlist_by_key_empty_key(self):
        """Test product list retrieval with empty key."""
        # Empty string
        await self.inventory_endpoints.get_productlist_by_key("")
        self.mock_client._make_api_request.assert_called_with(
            "/inventory/productlists/"
        )

    @pytest.mark.asyncio
    async def test_get_productlist_by_key_special_characters(self):
        """Test product list retrieval with special characters in key."""
        # Arrange
        product_list_key = "key-with-dashes_123"
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.inventory_endpoints.get_productlist_by_key(product_list_key)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            f"/inventory/productlists/{product_list_key}"
        )

    # Test list_all_productlists
    @pytest.mark.asyncio
    async def test_list_all_productlists_success(self):
        """Test successful listing of all product lists."""
        # Arrange
        expected_response = {
            "success": True,
            "results": [
                {
                    "productListId": 12345,
                    "productListKey": "test_key_1",
                    "createdAt": "2023-01-01T12:00:00Z",
                },
                {
                    "productListId": 67890,
                    "productListKey": "test_key_2",
                    "createdAt": "2023-01-02T12:00:00Z",
                },
            ],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.inventory_endpoints.list_all_productlists()

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/inventory/productLists"  # Note the capital L
        )

    @pytest.mark.asyncio
    async def test_list_all_productlists_empty_response(self):
        """Test listing all product lists with empty response."""
        # Arrange
        expected_response = {"success": True, "results": []}
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.inventory_endpoints.list_all_productlists()

        # Assert
        assert result == expected_response
        assert len(result["results"]) == 0

    @pytest.mark.asyncio
    async def test_list_all_productlists_authentication_error(self):
        """Test listing all product lists with authentication error."""
        # Arrange
        self.mock_client._make_api_request.side_effect = APIError(
            "Bearer token required", status_code=401
        )

        # Act & Assert
        with pytest.raises(APIError) as exc_info:
            await self.inventory_endpoints.list_all_productlists()

        assert exc_info.value.status_code == 401
        assert "Bearer token" in str(exc_info.value)

    # Test create_productlist
    @pytest.mark.asyncio
    async def test_create_productlist_success(self):
        """Test successful product list creation."""
        # Arrange
        product_list_data = {"name": "My Test List", "category": "Magic"}
        expected_response = {
            "success": True,
            "results": [{"productListKey": "new_list_key_12345"}],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.inventory_endpoints.create_productlist(product_list_data)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/inventory/productLists",  # Note the capital L
            method="POST",
            data=product_list_data,
        )

    @pytest.mark.asyncio
    async def test_create_productlist_no_data(self):
        """Test product list creation with no data."""
        # Arrange
        expected_response = {
            "success": True,
            "results": [{"productListKey": "default_list_key_12345"}],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.inventory_endpoints.create_productlist()

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/inventory/productLists", method="POST", data=None
        )

    @pytest.mark.asyncio
    async def test_create_productlist_empty_dict(self):
        """Test product list creation with empty dictionary."""
        # Arrange
        product_list_data = {}
        expected_response = {
            "success": True,
            "results": [{"productListKey": "empty_list_key_12345"}],
        }
        self.mock_client._make_api_request.return_value = expected_response

        # Act
        result = await self.inventory_endpoints.create_productlist(product_list_data)

        # Assert
        assert result == expected_response
        self.mock_client._make_api_request.assert_called_once_with(
            "/inventory/productLists", method="POST", data={}
        )

    @pytest.mark.asyncio
    async def test_create_productlist_permission_error(self):
        """Test product list creation with permission error."""
        # Arrange
        product_list_data = {"name": "Test List"}
        self.mock_client._make_api_request.side_effect = APIError(
            "Requires specific permissions - not accessible by all users",
            status_code=403,
        )

        # Act & Assert
        with pytest.raises(APIError) as exc_info:
            await self.inventory_endpoints.create_productlist(product_list_data)

        assert exc_info.value.status_code == 403
        assert "permissions" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_productlist_invalid_data(self):
        """Test product list creation with invalid data."""
        # Arrange
        product_list_data = {"invalid": "data_structure"}
        self.mock_client._make_api_request.side_effect = APIError(
            "Invalid request data", status_code=400
        )

        # Act & Assert
        with pytest.raises(APIError) as exc_info:
            await self.inventory_endpoints.create_productlist(product_list_data)

        assert exc_info.value.status_code == 400
        assert "Invalid" in str(exc_info.value)

    # Test initialization and client integration
    def test_inventory_endpoints_initialization(self):
        """Test InventoryEndpoints initialization."""
        # Test that client is properly stored
        assert self.inventory_endpoints.client == self.mock_client

        # Test that all expected methods exist
        expected_methods = [
            "get_productlist_by_id",
            "get_productlist_by_key",
            "list_all_productlists",
            "create_productlist",
        ]

        for method_name in expected_methods:
            assert hasattr(self.inventory_endpoints, method_name)
            assert callable(getattr(self.inventory_endpoints, method_name))

    @pytest.mark.asyncio
    async def test_correct_api_paths_used(self):
        """Test that correct API paths are used (addressing previous issues)."""
        # This test ensures we're using the correct paths as defined in API docs

        # Test product list by ID path
        await self.inventory_endpoints.get_productlist_by_id(123)
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/inventory/productlists/123"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test product list by key path (not /key/ prefix)
        await self.inventory_endpoints.get_productlist_by_key("test_key")
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/inventory/productlists/test_key"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test list all product lists path (capital L)
        await self.inventory_endpoints.list_all_productlists()
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/inventory/productLists"

        # Reset mock
        self.mock_client._make_api_request.reset_mock()

        # Test create product list path (capital L and POST method)
        await self.inventory_endpoints.create_productlist()
        calls = self.mock_client._make_api_request.call_args_list
        assert calls[0][0][0] == "/inventory/productLists"
        assert calls[0][1]["method"] == "POST"
