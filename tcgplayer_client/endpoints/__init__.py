"""
TCGplayer API endpoints organized by category.

This package contains all the API endpoint implementations organized into logical
groups:
- app: Application authorization and management
- catalog: Product and category operations
- pricing: Pricing and market data
- stores: Store management and operations (includes order management)
- inventory: Inventory and product list management
"""

from .app import AppEndpoints
from .catalog import CatalogEndpoints
from .inventory import InventoryEndpoints
from .pricing import PricingEndpoints
from .stores import StoreEndpoints

__all__ = [
    "AppEndpoints",
    "CatalogEndpoints",
    "PricingEndpoints",
    "StoreEndpoints",
    "InventoryEndpoints",
]
