"""
Verify remaining categories and products
"""
from models.product_model import ProductModel

categories = ProductModel.get_all_categories()
products = ProductModel.get_all_products()

print("=" * 60)
print("Current Database Contents")
print("=" * 60)
print(f"\nCategories ({len(categories)}):")
for cat in categories:
    print(f"  - {cat['name']} (ID: {cat['id']})")

print(f"\nProducts ({len(products)}):")
for prod in products:
    print(f"  - {prod['name']} - {prod['price']} RWF - Category: {prod.get('category_name', 'N/A')}")

print("\n" + "=" * 60)

