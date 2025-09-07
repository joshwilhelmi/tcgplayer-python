"""
Unit tests for the stores endpoints module.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from tcgplayer_client.endpoints.stores import StoreEndpoints


class TestStoreEndpoints:
    """Test cases for StoreEndpoints class."""

    def test_store_endpoints_initialization(self):
        """Test store endpoints initialization."""
        mock_client = MagicMock()
        stores = StoreEndpoints(mock_client)

        assert stores.client is mock_client

    # GROUP 1: BASIC STORE OPERATIONS

    @pytest.mark.asyncio
    async def test_search_stores_with_name(self):
        """Test searching stores with name filter."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": ["store1", "store2"]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.search_stores(name="Gamer")

        assert result == {"success": True, "results": ["store1", "store2"]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores", params={"name": "Gamer"}
        )

    @pytest.mark.asyncio
    async def test_search_stores_without_name(self):
        """Test searching stores without name filter."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": []}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.search_stores()

        assert result == {"success": True, "results": []}
        mock_client._make_api_request.assert_called_once_with("/stores", params={})

    @pytest.mark.asyncio
    async def test_get_store_info(self):
        """Test getting store info."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"storeKey": "test123"}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_store_info()

        assert result == {"success": True, "results": [{"storeKey": "test123"}]}
        mock_client._make_api_request.assert_called_once_with("/stores/self")

    @pytest.mark.asyncio
    async def test_get_store_address(self):
        """Test getting store address."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"address": "123 Main St"}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_store_address("test_store_key")

        assert result == {"success": True, "results": [{"address": "123 Main St"}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/address"
        )

    @pytest.mark.asyncio
    async def test_set_store_status(self):
        """Test setting store status."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        stores = StoreEndpoints(mock_client)
        result = await stores.set_store_status("test_store_key", "open")

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/status/open", method="PUT"
        )

    # GROUP 2: INVENTORY MANAGEMENT

    @pytest.mark.asyncio
    async def test_get_product_inventory_quantities(self):
        """Test getting product inventory quantities."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={
                "success": True,
                "results": [{"productId": 123, "totalQuantity": 10}],
            }
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_product_inventory_quantities("test_store_key", 123)

        assert result == {
            "success": True,
            "results": [{"productId": 123, "totalQuantity": 10}],
        }
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/inventory/products/123/quantity"
        )

    @pytest.mark.asyncio
    async def test_list_product_summary(self):
        """Test listing product summary."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={
                "success": True,
                "results": [{"productId": 123, "name": "Card"}],
            }
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.list_product_summary("test_store_key")

        assert result == {
            "success": True,
            "results": [{"productId": 123, "name": "Card"}],
        }
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/inventory/products"
        )

    @pytest.mark.asyncio
    async def test_get_sku_quantity(self):
        """Test getting SKU quantity."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"skuId": 456, "quantity": 5}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_sku_quantity("test_store_key", 456)

        assert result == {"success": True, "results": [{"skuId": 456, "quantity": 5}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/inventory/skus/456/quantity"
        )

    @pytest.mark.asyncio
    async def test_update_sku_inventory(self):
        """Test updating SKU inventory."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        stores = StoreEndpoints(mock_client)
        result = await stores.update_sku_inventory("test_store_key", 456, 10.99, 5, 1)

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/inventory/skus/456",
            method="PUT",
            data={"price": 10.99, "quantity": 5, "channelId": 1},
        )

    @pytest.mark.asyncio
    async def test_update_sku_inventory_price(self):
        """Test updating SKU inventory price."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        stores = StoreEndpoints(mock_client)
        result = await stores.update_sku_inventory_price(
            "test_store_key", 456, 15.99, 1
        )

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/inventory/skus/456/price",
            method="PUT",
            data={"price": 15.99, "channelId": 1},
        )

    @pytest.mark.asyncio
    async def test_increment_sku_inventory_quantity(self):
        """Test incrementing SKU inventory quantity."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        stores = StoreEndpoints(mock_client)
        result = await stores.increment_sku_inventory_quantity(
            "test_store_key", 456, 3, 1
        )

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/inventory/skus/456/quantity",
            method="POST",
            data={"quantity": 3, "channelId": 1},
        )

    @pytest.mark.asyncio
    async def test_batch_update_store_sku_prices(self):
        """Test batch updating store SKU prices."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        updates = [{"skuId": 456, "price": 12.99}, {"skuId": 789, "price": 8.50}]
        stores = StoreEndpoints(mock_client)
        result = await stores.batch_update_store_sku_prices("test_store_key", updates)

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/inventory/skus/batch", method="POST", data=updates
        )

    @pytest.mark.asyncio
    async def test_list_sku_list_price(self):
        """Test listing SKU list prices."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"skuId": 456, "price": 10.99}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.list_sku_list_price("test_store_key")

        assert result == {"success": True, "results": [{"skuId": 456, "price": 10.99}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/inventory/skuprices"
        )

    # GROUP 3: CUSTOMER MANAGEMENT

    @pytest.mark.asyncio
    async def test_get_customer_summary(self):
        """Test getting customer summary."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"totalOrders": 5}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_customer_summary("test_store_key", "customer_token")

        assert result == {"success": True, "results": [{"totalOrders": 5}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/customers/customer_token"
        )

    @pytest.mark.asyncio
    async def test_search_store_customers(self):
        """Test searching store customers."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"customerId": 123}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.search_store_customers("test_store_key")

        assert result == {"success": True, "results": [{"customerId": 123}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/customers"
        )

    @pytest.mark.asyncio
    async def test_get_customer_addresses(self):
        """Test getting customer addresses."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"address": "123 Main St"}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_customer_addresses("test_store_key", "customer_token")

        assert result == {"success": True, "results": [{"address": "123 Main St"}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/customers/customer_token/addresses"
        )

    @pytest.mark.asyncio
    async def test_get_customer_orders(self):
        """Test getting customer orders."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"orderId": 789}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_customer_orders("test_store_key", "customer_token")

        assert result == {"success": True, "results": [{"orderId": 789}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/customers/customer_token/orders"
        )

    @pytest.mark.asyncio
    async def test_get_store_feedback(self):
        """Test getting store feedback."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"rating": 4.5}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_store_feedback("test_store_key")

        assert result == {"success": True, "results": [{"rating": 4.5}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/feedback"
        )

    # GROUP 4: ORDER MANAGEMENT

    @pytest.mark.asyncio
    async def test_search_orders(self):
        """Test searching orders."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"orderId": 123}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.search_orders("test_store_key")

        assert result == {"success": True, "results": [{"orderId": 123}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/orders"
        )

    @pytest.mark.asyncio
    async def test_get_order_tracking_numbers(self):
        """Test getting order tracking numbers."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"trackingNumber": "ABC123"}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_order_tracking_numbers("test_store_key", "ORD123")

        assert result == {"success": True, "results": [{"trackingNumber": "ABC123"}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/orders/ORD123/tracking"
        )

    @pytest.mark.asyncio
    async def test_add_order_tracking_number(self):
        """Test adding order tracking number."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        tracking_data = {"trackingNumber": "XYZ789", "carrier": "UPS"}
        stores = StoreEndpoints(mock_client)
        result = await stores.add_order_tracking_number(
            "test_store_key", "ORD123", tracking_data
        )

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/orders/ORD123/tracking",
            method="POST",
            data=tracking_data,
        )

    @pytest.mark.asyncio
    async def test_get_order_manifest(self):
        """Test getting order manifest."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"manifestId": 456}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_order_manifest("test_store_key")

        assert result == {"success": True, "results": [{"manifestId": 456}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/orders/manifest"
        )

    @pytest.mark.asyncio
    async def test_get_order_details(self):
        """Test getting order details."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={
                "success": True,
                "results": [{"orderId": 789, "total": 25.99}],
            }
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_order_details("test_store_key", "ORD123,ORD456")

        assert result == {
            "success": True,
            "results": [{"orderId": 789, "total": 25.99}],
        }
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/orders/ORD123,ORD456"
        )

    @pytest.mark.asyncio
    async def test_get_order_items(self):
        """Test getting order items."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"itemId": 101, "quantity": 2}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_order_items("test_store_key", "ORD123")

        assert result == {"success": True, "results": [{"itemId": 101, "quantity": 2}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/orders/ORD123/items"
        )

    @pytest.mark.asyncio
    async def test_get_order_feedback(self):
        """Test getting order feedback."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"feedback": "Great service!"}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_order_feedback("test_store_key", "ORD123")

        assert result == {"success": True, "results": [{"feedback": "Great service!"}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/orders/ORD123/feedback"
        )

    # GROUP 5: BUYLIST OPERATIONS

    @pytest.mark.asyncio
    async def test_batch_update_store_buylist_prices(self):
        """Test batch updating store buylist prices."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        buylist_updates = [
            {"skuId": 456, "buyPrice": 8.99},
            {"skuId": 789, "buyPrice": 5.50},
        ]
        stores = StoreEndpoints(mock_client)
        result = await stores.batch_update_store_buylist_prices(
            "test_store_key", buylist_updates
        )

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/buylist/skus/batch",
            method="POST",
            data=buylist_updates,
        )

    @pytest.mark.asyncio
    async def test_create_sku_buylist(self):
        """Test creating SKU buylist entry."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        buylist_data = {"buyPrice": 12.50, "quantity": 10}
        stores = StoreEndpoints(mock_client)
        result = await stores.create_sku_buylist("test_store_key", 456, buylist_data)

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/buylist/skus/456", method="PUT", data=buylist_data
        )

    @pytest.mark.asyncio
    async def test_update_sku_buylist_price(self):
        """Test updating SKU buylist price."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        price_data = {"buyPrice": 15.25}
        stores = StoreEndpoints(mock_client)
        result = await stores.update_sku_buylist_price(
            "test_store_key", 456, price_data
        )

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/buylist/skus/456/price",
            method="PUT",
            data=price_data,
        )

    @pytest.mark.asyncio
    async def test_update_sku_buylist_quantity(self):
        """Test updating SKU buylist quantity."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(return_value={"success": True})

        quantity_data = {"quantity": 25}
        stores = StoreEndpoints(mock_client)
        result = await stores.update_sku_buylist_quantity(
            "test_store_key", 456, quantity_data
        )

        assert result == {"success": True}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/buylist/skus/456/quantity",
            method="PUT",
            data=quantity_data,
        )

    @pytest.mark.asyncio
    async def test_get_buylist_categories(self):
        """Test getting buylist categories."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={
                "success": True,
                "results": [{"categoryId": 1, "name": "Magic"}],
            }
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_buylist_categories("test_store_key")

        assert result == {
            "success": True,
            "results": [{"categoryId": 1, "name": "Magic"}],
        }
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/buylist/categories"
        )

    @pytest.mark.asyncio
    async def test_get_buylist_groups(self):
        """Test getting buylist groups."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={
                "success": True,
                "results": [{"groupId": 1, "name": "Core Set"}],
            }
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_buylist_groups("test_store_key")

        assert result == {
            "success": True,
            "results": [{"groupId": 1, "name": "Core Set"}],
        }
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/buylist/groups"
        )

    @pytest.mark.asyncio
    async def test_get_store_buylist_settings(self):
        """Test getting store buylist settings."""
        mock_client = MagicMock()
        mock_client._make_api_request = AsyncMock(
            return_value={"success": True, "results": [{"enabled": True}]}
        )

        stores = StoreEndpoints(mock_client)
        result = await stores.get_store_buylist_settings("test_store_key")

        assert result == {"success": True, "results": [{"enabled": True}]}
        mock_client._make_api_request.assert_called_once_with(
            "/stores/test_store_key/buylist/settings"
        )
