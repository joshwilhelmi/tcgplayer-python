# 🚨 TESTING SAFETY GUIDELINES

## Critical Incident: Live Data Modification

**Date**: September 7, 2025  
**Issue**: During endpoint testing, we accidentally modified live store pricing data  
**Impact**: Changed SKU 1195969 price to $25.99 in Game Goblins store (3d05ef67)  
**Status**: Store owner contacted for remediation  

## MANDATORY SAFETY RULES FOR FUTURE TESTING

### ❌ NEVER TEST THESE OPERATIONS ON LIVE DATA

**Store Management - Write Operations:**
- `update_sku_inventory_price()` 
- `update_sku_inventory()`
- `increment_sku_inventory_quantity()`
- `batch_update_store_sku_prices()`
- `batch_update_store_buylist_prices()`
- `create_sku_buylist()`
- `update_sku_buylist_price()`
- `update_sku_buylist_quantity()`
- `create_productlist()`
- `set_store_status()`
- `add_order_tracking_number()`

### ✅ SAFE TO TEST - READ-ONLY OPERATIONS

**Catalog Endpoints:** All safe (read-only)
**Pricing Endpoints:** All safe (read-only)
**Store Endpoints - Read Operations:**
- `get_store_info()`
- `search_stores()`
- `get_store_address()`
- `list_product_summary()`
- `list_all_groups()`
- `list_all_categories()`
- etc.

### 🛡️ TESTING METHODOLOGY UPDATES

#### For Write Operations:
1. **Mock the call** - Don't actually execute
2. **Test method signature only** - Verify parameters are correct
3. **Use test data** - Never use real SKU IDs or store data
4. **Sandbox environment** - If available, use test instance

#### Example Safe Testing:
```python
# ❌ DANGEROUS - Actually modifies live data
await client.endpoints.stores.update_sku_inventory_price(store_key, sku_id, 25.99, 1)

# ✅ SAFE - Test method signature only
try:
    # Don't actually call, just verify method exists and parameters
    method = client.endpoints.stores.update_sku_inventory_price
    assert callable(method), "Method should exist"
    print("✅ Method signature valid")
except Exception as e:
    print(f"❌ Method issue: {e}")
```

#### Safe Comprehensive Testing Pattern:
```python
# Categorize endpoints by safety
SAFE_ENDPOINTS = [
    # All read-only operations
    ("Get Store Info", lambda: client.endpoints.stores.get_store_info()),
    ("List Categories", lambda: client.endpoints.catalog.list_all_categories()),
    # ... other read operations
]

UNSAFE_ENDPOINTS = [
    # Write operations - TEST SIGNATURE ONLY
    ("Update SKU Price", "MOCK_ONLY - Would modify live data"),
    ("Create Buylist", "MOCK_ONLY - Would modify live data"),
    # ... other write operations
]

# Test safe endpoints normally
for name, test_func in SAFE_ENDPOINTS:
    try:
        result = await test_func()
        print(f"✅ {name}: {'PASS' if result.get('success') else 'FAIL'}")
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")

# Handle unsafe endpoints safely
for name, reason in UNSAFE_ENDPOINTS:
    print(f"🛡️ {name}: SKIPPED - {reason}")
```

## CONTACT INFORMATION

**Store Owner**: Game Goblins  
**Email**: tcglittlerock@gamegoblins.com  
**Store Key**: 3d05ef67  
**Affected SKU**: 1195969 (set to $25.99 - needs verification/revert)  

## FUTURE PREVENTION

1. **Code Review**: All testing scripts must be reviewed before execution
2. **Environment Separation**: Use test/sandbox environments when available  
3. **Read-Only by Default**: Assume all operations are dangerous unless proven safe
4. **Mock Write Operations**: Never execute actual write calls during testing
5. **Explicit Consent**: Require explicit approval before any write operation testing