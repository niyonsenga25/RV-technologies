"""
Script to remove old categories and products, keeping only html-version data
"""
import mysql.connector
from config import Config

# Categories to keep (from html-version)
categories_to_keep = ["Laptops", "Computers", "Printers", "Storage", "Networking", "Power"]

# Products to keep (from html-version)
products_to_keep = [
    "HP EliteBook 840 G5 i7",
    "HP EliteBook 830 i5",
    "HP Envy X360 i7",
    "HP 290 Desktop",
    "EPSON L3250",
    "Epson L3210",
    "Canon ImageRunner 2224if",
    "XPRINTER 80",
    "SSD 512GB",
    "Flash Drive 64GB",
    "CAT6 SFTP Cable",
    "UTP CAT6 Cable",
    "APC SMART UPS 750V"
]

def cleanup_data():
    """Remove old categories and products"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        
        cursor = connection.cursor()
        
        print("=" * 60)
        print("Cleaning Up Old Data")
        print("=" * 60)
        
        # Step 1: Delete products not in the keep list
        print("\n1. Removing old products...")
        placeholders = ','.join(['%s'] * len(products_to_keep))
        delete_products_query = f"""
            DELETE FROM products 
            WHERE name NOT IN ({placeholders})
        """
        cursor.execute(delete_products_query, products_to_keep)
        deleted_products = cursor.rowcount
        print(f"   [OK] Deleted {deleted_products} old products")
        
        # Step 2: Delete categories not in the keep list
        print("\n2. Removing old categories...")
        placeholders = ','.join(['%s'] * len(categories_to_keep))
        delete_categories_query = f"""
            DELETE FROM categories 
            WHERE name NOT IN ({placeholders})
        """
        cursor.execute(delete_categories_query, categories_to_keep)
        deleted_categories = cursor.rowcount
        print(f"   [OK] Deleted {deleted_categories} old categories")
        
        # Step 3: Clean up orphaned data
        print("\n3. Cleaning up orphaned data...")
        
        # Delete cart items for deleted products
        cursor.execute("""
            DELETE FROM cart 
            WHERE product_id NOT IN (SELECT id FROM products)
        """)
        deleted_cart_items = cursor.rowcount
        print(f"   [OK] Deleted {deleted_cart_items} orphaned cart items")
        
        # Delete order items for deleted products
        cursor.execute("""
            DELETE FROM order_items 
            WHERE product_id NOT IN (SELECT id FROM products)
        """)
        deleted_order_items = cursor.rowcount
        print(f"   [OK] Deleted {deleted_order_items} orphaned order items")
        
        # Delete reviews for deleted products
        cursor.execute("""
            DELETE FROM reviews 
            WHERE product_id NOT IN (SELECT id FROM products)
        """)
        deleted_reviews = cursor.rowcount
        print(f"   [OK] Deleted {deleted_reviews} orphaned reviews")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("Cleanup completed successfully!")
        print("=" * 60)
        print(f"\nRemaining categories: {len(categories_to_keep)}")
        print(f"Remaining products: {len(products_to_keep)}")
        
    except mysql.connector.Error as e:
        print(f"\n[ERROR] Database Error: {e}")
        print("Please check your database configuration in config.py")
        if connection:
            connection.rollback()
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        if connection:
            connection.rollback()
            cursor.close()
            connection.close()

if __name__ == "__main__":
    cleanup_data()

