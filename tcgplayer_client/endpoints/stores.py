"""
Store endpoints for TCGplayer API.

This module contains all store-related operations including:
- Store management and settings
- Customer management
- Product inventory and pricing
- Order management and tracking
- Buylist operations
- Batch operations and pricing
"""

from typing import Any, Dict, List, Optional

from ..client import TCGplayerClient


class StoreEndpoints:
    """Store-related API endpoints."""

    def __init__(self, client: TCGplayerClient):
        """
        Initialize store endpoints.

        Args:
            client: TCGplayer client instance
        """
        self.client = client

    # GROUP 1: BASIC STORE OPERATIONS

    async def search_stores(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns a collection of storeKey values based on the search parameters.

        Args:
            name: Filters stores by name (e.g., 'Gamer')

        Returns:
            Dict containing search results with storeKey values
        """
        params = {}
        if name is not None:
            params["name"] = name

        return await self.client._make_api_request("/stores", params=params)

    async def get_store_info(self) -> Dict[str, Any]:
        """
        Return general information about the current Store associated with the
        current bearer token.

        Returns:
            Dict containing store information
        """
        self.client._check_store_enabled("get_store_info")
        return await self.client._make_api_request("/stores/self")

    async def get_store_address(self, store_key: str) -> Dict[str, Any]:
        """
        Return address information about the Store specified by the storeKey.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing store address information
        """
        return await self.client._make_api_request(f"/stores/{store_key}/address")

    async def set_store_status(self, store_key: str, status: str) -> Dict[str, Any]:
        """
        Set the status of a store.

        Args:
            store_key: Unique identifier for the store
            status: Status to set for the store

        Returns:
            Dict containing operation result
        """
        self.client._check_store_enabled("set_store_status")
        return await self.client._make_api_request(
            f"/stores/{store_key}/status/{status}", method="PUT"
        )

    # GROUP 2: INVENTORY MANAGEMENT

    async def get_product_inventory_quantities(
        self, store_key: str, product_id: int
    ) -> Dict[str, Any]:
        """
        Gets inventory quantities for a specific product at a store.

        Args:
            store_key: Unique identifier for the store
            product_id: Specific product identifier to retrieve inventory for

        Returns:
            Dict containing product inventory quantities
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/products/{product_id}/quantity"
        )

    async def list_product_summary(self, store_key: str) -> Dict[str, Any]:
        """
        Returns all products currently for sale in a specific store.

        Args:
            store_key: Store identifier

        Returns:
            Dict containing product summary information
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/products"
        )

    async def get_sku_quantity(self, store_key: str, sku_id: int) -> Dict[str, Any]:
        """
        Returns quantity of a specific SKU in store inventory.

        Args:
            store_key: Store identifier
            sku_id: Specific SKU identifier

        Returns:
            Dict containing SKU quantity information
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/skus/{sku_id}/quantity"
        )

    async def update_sku_inventory(
        self, store_key: str, sku_id: int, price: float, quantity: int, channel_id: int
    ) -> Dict[str, Any]:
        """
        Adds or updates a SKU in the store's inventory.

        Args:
            store_key: Store identifier
            sku_id: Specific SKU identifier
            price: Price for the SKU
            quantity: Quantity for the SKU
            channel_id: Channel identifier

        Returns:
            Dict containing operation result
        """
        data = {"price": price, "quantity": quantity, "channelId": channel_id}
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/skus/{sku_id}", method="PUT", data=data
        )

    async def update_sku_inventory_price(
        self, store_key: str, sku_id: int, price: float, channel_id: int
    ) -> Dict[str, Any]:
        """
        Updates pricing for a single SKU in the authenticated store.

        Args:
            store_key: Store identifier
            sku_id: SKU identifier
            price: New price for the SKU
            channel_id: Channel identifier

        Returns:
            Dict containing operation result
        """
        data = {"price": price, "channelId": channel_id}
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/skus/{sku_id}/price",
            method="PUT",
            data=data,
        )

    async def increment_sku_inventory_quantity(
        self, store_key: str, sku_id: int, quantity: int, channel_id: int
    ) -> Dict[str, Any]:
        """
        Increment SKU inventory quantity.

        Args:
            store_key: Store identifier
            sku_id: SKU identifier
            quantity: Quantity to increment
            channel_id: Channel identifier

        Returns:
            Dict containing operation result
        """
        data = {"quantity": quantity, "channelId": channel_id}
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/skus/{sku_id}/quantity",
            method="POST",
            data=data,
        )

    async def batch_update_store_sku_prices(
        self, store_key: str, sku_updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Batch update store SKU prices.

        Args:
            store_key: Store identifier
            sku_updates: List of SKU price updates

        Returns:
            Dict containing batch operation result
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/skus/batch", method="POST", data=sku_updates
        )

    async def list_sku_list_price(self, store_key: str) -> Dict[str, Any]:
        """
        List SKU list prices for a store.

        Args:
            store_key: Store identifier

        Returns:
            Dict containing SKU list prices
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/skuprices"
        )

    # GROUP 3: CUSTOMER MANAGEMENT

    async def get_customer_summary(self, store_key: str, token: str) -> Dict[str, Any]:
        """
        Returns the total number of orders and total product dollar amount for
        all orders a customer has place with the seller.

        Args:
            store_key: Unique store identifier
            token: Unique seller and customer combination

        Returns:
            Dict containing customer summary information
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/customers/{token}"
        )

    async def search_store_customers(
        self,
        store_key: str,
        name: str = None,
        email: str = None,
        offset: int = 0,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search Store Customers.

        Args:
            store_key: A unique key used to identify the caller of the API
            name: A string of characters representing the first name and/or last name of the customer being searched for. Use format "firstName,lastName"
            email: The email of the customer
            offset: Used for paging. The number of records to skip. Default is 0
            limit: Used for paging. The maximum number of records to return. Default is 10

        Returns:
            Dict containing customer search results
        """
        params = {}
        if name is not None:
            params["name"] = name
        if email is not None:
            params["email"] = email
        if offset != 0:
            params["offset"] = offset
        if limit != 10:
            params["limit"] = limit
            
        return await self.client._make_api_request(
            f"/stores/{store_key}/customers",
            params=params
        )

    async def get_customer_addresses(
        self, store_key: str, token: str
    ) -> Dict[str, Any]:
        """
        Returns the shipping addresses associated with the orders a customer
        has placed with the seller.

        Args:
            store_key: Unique store identifier
            token: Unique seller-customer combination identifier

        Returns:
            Dict containing customer addresses
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/customers/{token}/addresses"
        )

    async def get_customer_orders(self, store_key: str, token: str) -> Dict[str, Any]:
        """
        Returns a list of orders containing the total product quantity and
        total product dollar amount for each order a customer has placed with
        the seller.

        Args:
            store_key: Unique store identifier
            token: Unique seller and customer combination

        Returns:
            Dict containing customer orders
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/customers/{token}/orders"
        )

    async def get_store_feedback(self, store_key: str) -> Dict[str, Any]:
        """
        Get store feedback information.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing store feedback
        """
        return await self.client._make_api_request(f"/stores/{store_key}/feedback")

    # GROUP 4: ORDER MANAGEMENT

    async def search_orders(self, store_key: str) -> Dict[str, Any]:
        """
        Search orders for a store.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing order search results
        """
        return await self.client._make_api_request(f"/stores/{store_key}/orders")

    async def get_order_tracking_numbers(
        self, store_key: str, order_number: str
    ) -> Dict[str, Any]:
        """
        Get order tracking numbers.

        Args:
            store_key: Unique identifier for the store
            order_number: Order number

        Returns:
            Dict containing tracking numbers
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_number}/tracking"
        )

    async def add_order_tracking_number(
        self, store_key: str, order_number: str, tracking_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add order tracking number.

        Args:
            store_key: Unique identifier for the store
            order_number: Order number
            tracking_data: Tracking information

        Returns:
            Dict containing operation result
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_number}/tracking",
            method="POST",
            data=tracking_data,
        )

    async def get_order_manifest(self, store_key: str) -> Dict[str, Any]:
        """
        Get order manifest for a store.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing order manifest
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/manifest"
        )

    async def get_order_details(
        self, store_key: str, order_numbers: str
    ) -> Dict[str, Any]:
        """
        Get order details.

        Args:
            store_key: Unique identifier for the store
            order_numbers: Order numbers (comma-separated)

        Returns:
            Dict containing order details
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_numbers}"
        )

    async def get_order_items(
        self, store_key: str, order_number: str
    ) -> Dict[str, Any]:
        """
        Get order items.

        Args:
            store_key: Unique identifier for the store
            order_number: Order number

        Returns:
            Dict containing order items
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_number}/items"
        )

    async def get_order_feedback(
        self, store_key: str, order_number: str
    ) -> Dict[str, Any]:
        """
        Get order feedback.

        Args:
            store_key: Unique identifier for the store
            order_number: Order number

        Returns:
            Dict containing order feedback
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/orders/{order_number}/feedback"
        )

    # GROUP 5: BUYLIST OPERATIONS

    async def batch_update_store_buylist_prices(
        self, store_key: str, buylist_updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Batch update store buylist prices.

        Args:
            store_key: Unique identifier for the store
            buylist_updates: List of buylist price updates

        Returns:
            Dict containing batch operation result
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/skus/batch",
            method="POST",
            data=buylist_updates,
        )

    async def create_sku_buylist(
        self, store_key: str, sku_id: int, buylist_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create SKU buylist entry.

        Args:
            store_key: Unique identifier for the store
            sku_id: SKU identifier
            buylist_data: Buylist data

        Returns:
            Dict containing operation result
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/skus/{sku_id}",
            method="PUT",
            data=buylist_data,
        )

    async def update_sku_buylist_price(
        self, store_key: str, sku_id: int, price_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update SKU buylist price.

        Args:
            store_key: Unique identifier for the store
            sku_id: SKU identifier
            price_data: Price data

        Returns:
            Dict containing operation result
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/skus/{sku_id}/price",
            method="PUT",
            data=price_data,
        )

    async def update_sku_buylist_quantity(
        self, store_key: str, sku_id: int, quantity_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update SKU buylist quantity.

        Args:
            store_key: Unique identifier for the store
            sku_id: SKU identifier
            quantity_data: Quantity data

        Returns:
            Dict containing operation result
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/skus/{sku_id}/quantity",
            method="PUT",
            data=quantity_data,
        )

    async def get_buylist_categories(self, store_key: str) -> Dict[str, Any]:
        """
        Get buylist categories.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing buylist categories
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/categories"
        )

    async def get_buylist_groups(self, store_key: str) -> Dict[str, Any]:
        """
        Get buylist groups.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing buylist groups
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/groups"
        )

    async def get_store_buylist_settings(self, store_key: str) -> Dict[str, Any]:
        """
        Get store buylist settings.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing buylist settings
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/settings"
        )

    # GROUP 6: CATALOG & SEARCH

    async def list_all_groups(self, store_key: str) -> Dict[str, Any]:
        """
        List all groups for a store.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing all groups
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/groups"
        )

    async def list_product_skus(
        self, store_key: str, product_id: int
    ) -> Dict[str, Any]:
        """
        List product SKUs for a store.

        Args:
            store_key: Unique identifier for the store
            product_id: Product identifier

        Returns:
            Dict containing product SKUs
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/products/{product_id}/skus"
        )

    async def list_related_products(
        self, store_key: str, product_id: int
    ) -> Dict[str, Any]:
        """
        List related products for a store.

        Args:
            store_key: Unique identifier for the store
            product_id: Product identifier

        Returns:
            Dict containing related products
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/products/{product_id}/relatedproducts"
        )

    async def list_all_categories(self, store_key: str) -> Dict[str, Any]:
        """
        List all categories for a store.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing all categories
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/categories"
        )

    async def list_store_channels(
        self, store_key: str, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        List store channels.

        Args:
            store_key: Unique identifier for the store
            offset: Used for paging. The number of Channels to skip. Default is 0.
            limit: Used for paging. The maximum number of Channels to return. Default is 10.

        Returns:
            Dict containing store channels
        """
        params = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
            
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/channels", params=params
        )

    async def get_store_buylist_products_for_kiosk(
        self,
        store_key: str,
        search_term: str = None,
        offset: int = None,
        limit: int = None,
        sort_direction: str = None,
        category_id: int = None
    ) -> Dict[str, Any]:
        """
        Get a Store's Buylist Products for Kiosk use.

        Args:
            store_key: A unique key used to identify the caller of the API
            search_term: The term which must be contained in either the Product Name or Set Name of the Products
            offset: The number of Products to skip in the initial result set
            limit: The maximum number of Products to be returned
            sort_direction: The direction of the sort to be applied. Options are ASC or DESC. Defaults to ASC
            category_id: If provided will only return Buylist Products in the Category

        Returns:
            Dict containing buylist products for kiosk
        """
        params = {}
        if search_term is not None:
            params["searchTerm"] = search_term
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if sort_direction is not None:
            params["sortDirection"] = sort_direction
        if category_id is not None:
            params["categoryId"] = category_id
            
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/products",
            params=params
        )

    async def get_product_conditions_for_buylist(
        self, store_key: str, product_id: int
    ) -> Dict[str, Any]:
        """
        Get the Product Conditions for a Product on a Store's Buylist.

        Args:
            store_key: Unique identifier for the store
            product_id: Product identifier

        Returns:
            Dict containing product conditions for buylist
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/buylist/{product_id}"
        )

    async def list_product_summary_by_category(
        self, store_key: str, category_id: int, search_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        List Product Summary By Category.

        Args:
            store_key: Unique identifier for the store
            category_id: Category identifier
            search_data: Search criteria

        Returns:
            Dict containing product summary by category
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/categories/{category_id}/search",
            method="POST",
            data=search_data,
        )

    async def list_catalog_objects(
        self, store_key: str, q: str, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        List Catalog Objects.

        Args:
            store_key: Unique identifier for the store
            q: The string to search for in Product, Category, and Group names.
            limit: Used for paging. The maximum number of SearchResults to return. Default is 10.

        Returns:
            Dict containing catalog objects
        """
        params = {"q": q}
        if limit is not None:
            params["limit"] = limit
            
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/search", params=params
        )

    # GROUP 7: BATCH OPERATIONS & PRICING

    async def get_sku_list_price(
        self, store_key: str, sku_list_price_id: int
    ) -> Dict[str, Any]:
        """
        Get SKU List Price.

        Args:
            store_key: Unique identifier for the store
            sku_list_price_id: SKU list price identifier

        Returns:
            Dict containing SKU list price
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/skuprices/{sku_list_price_id}"
        )

    async def get_store_info_by_keys(self, store_keys: str) -> Dict[str, Any]:
        """
        Get Store Info by store keys.

        Args:
            store_keys: Store keys (comma-separated)

        Returns:
            Dict containing store information
        """
        return await self.client._make_api_request(f"/stores/{store_keys}")

    async def get_free_shipping_option(self, store_key: str) -> Dict[str, Any]:
        """
        Get Free Shipping Option.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing free shipping settings
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/freeshipping/settings"
        )

    async def list_shipping_options(
        self, store_key: str, product_id: int
    ) -> Dict[str, Any]:
        """
        List Shipping Options.

        Args:
            store_key: Unique identifier for the store
            product_id: Product identifier

        Returns:
            Dict containing shipping options
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/products/{product_id}/shippingoptions"
        )

    async def list_top_sold_products(self, store_key: str) -> Dict[str, Any]:
        """
        List Top Sold Products.

        Args:
            store_key: Unique identifier for the store

        Returns:
            Dict containing top sold products
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/topsales"
        )

    async def search_top_sold_products(
        self, store_key: str, search_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Search Top Sold Products.

        Args:
            store_key: Unique identifier for the store
            search_data: Search criteria

        Returns:
            Dict containing top sold products search results
        """
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/topsalessearch",
            method="POST",
            data=search_data,
        )

    async def search_custom_listings(self, store_key: str, photo_id: int) -> Dict[str, Any]:
        """
        Search Custom Listings.

        Args:
            store_key: Unique identifier for the store
            photo_id: The photo ID for the custom listing search (required)

        Returns:
            Dict containing custom listings
        """
        params = {"photoId": photo_id}
        return await self.client._make_api_request(
            f"/stores/{store_key}/inventory/customListings",
            params=params
        )
