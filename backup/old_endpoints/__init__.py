"""
TCGPlayer API endpoints organized by category.

This package contains all the API endpoint implementations organized into logical
groups:
- catalog: Product and category operations
- pricing: Pricing and market data
- stores: Store management and operations
- orders: Order processing and management
- inventory: Inventory and product list management
"""

from .catalog import CatalogEndpoints
from .inventory import InventoryEndpoints
from .orders import OrderEndpoints
from .pricing import PricingEndpoints
from .stores import StoreEndpoints

__all__ = [
    "CatalogEndpoints",
    "PricingEndpoints",
    "StoreEndpoints",
    "OrderEndpoints",
    "InventoryEndpoints",
]
