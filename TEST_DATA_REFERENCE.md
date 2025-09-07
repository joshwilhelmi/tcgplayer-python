# TCGplayer API Test Data Reference

This file contains real example data from the official TCGplayer API documentation that can be used for testing and development.

## Real Test Data from Official Documentation

### Categories
- **Magic: The Gathering**: categoryId `1` (most common, used as default)
- **YuGiOh**: categoryId `2`
- **Pokemon**: categoryId `3`
- **Axis & Allies**: categoryId `4`

### Products
- **Totodile**: productId `90000` (Pokemon card)
- **Mega Rayquaza Collection**: productId `100500` (Pokemon product)
- **Harry Potter: Hedwig Funko Pop**: productId `182307` (GTIN: 889698355100)

### Groups/Sets
- **Early Sets**: groupIds `1`, `2`, `3`
- **Specific Sets**: groupIds `1940`, `1956`

### GTIN Codes
- **Valid GTIN**: `889698355100` (Harry Potter: Hedwig Funko Pop, productId: 182307)

### SKUs
- Use productId `90000` or `100500` to get real SKU lists via `/catalog/products/{productId}/skus`

## Usage Examples

### Working API Calls
```python
# Get categories (always works)
await client.endpoints.catalog.list_all_categories()

# Get specific category details
await client.endpoints.catalog.get_category_details([1, 2, 3])

# Get groups for Magic: The Gathering
await client.endpoints.catalog.list_all_category_groups(1)

# Get product details
await client.endpoints.catalog.get_product_details([90000, 100500])

# Get product by GTIN
await client.endpoints.catalog.get_product_details_by_gtin("889698355100")

# Get product SKUs
await client.endpoints.catalog.list_product_skus(90000)

# Get group details
await client.endpoints.catalog.get_group_details([1940, 1956])

# Pricing with real SKU chain
skus_response = await client.endpoints.catalog.list_product_skus(90000)
sku_ids = [sku['skuId'] for sku in skus_response['results']]

# Get SKU market prices (requires SKU IDs from above)
await client.endpoints.pricing.get_sku_market_prices(sku_ids)

# Get SKU buylist prices (requires SKU IDs from above)
await client.endpoints.pricing.get_sku_buylist_prices(sku_ids)

# Group media with real group chain
groups_response = await client.endpoints.catalog.list_all_category_groups(1)
group_ids = [group['groupId'] for group in groups_response['results']]

# Get group media (requires group IDs from above, some groups may have no media)
await client.endpoints.catalog.list_all_group_media(group_ids[0])
```

### Test Data Chain Dependencies
1. **Categories** → Groups → Products → SKUs
2. **Start with category 1** (Magic) to get valid group IDs
3. **Use group IDs** to find products in that group
4. **Use product IDs** to get SKUs for that product

## Data Sources
All data scraped from official TCGplayer API documentation:
- https://docs.tcgplayer.com/reference/catalog_getcategories-1
- https://docs.tcgplayer.com/reference/catalog_getproduct-1  
- https://docs.tcgplayer.com/reference/catalog_getproductbygtin-1
- https://docs.tcgplayer.com/reference/catalog_getgroup-1

## Notes
- Category 1 (Magic: The Gathering) is the most reliable for testing
- Not all products have GTINs - 889698355100 is confirmed to work
- Product IDs 90000 and 100500 are confirmed working examples
- Use these IDs instead of arbitrary test data for more realistic testing