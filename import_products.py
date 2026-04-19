"""
Script to import products and categories from html-version/data.js into the database
"""
import mysql.connector
from config import Config
import os

# Products data from data.js
products_data = [
    {
        "id": 1,
        "name": "HP EliteBook 840 G5 i7",
        "description": "Professional business laptop with Intel Core i7 processor, premium build quality. Perfect for demanding business applications and multitasking.",
        "price": 500000,
        "category": "Laptops",
        "image": "EliteBook 840 G5 i7 ; 500,000 RWF.jpg",
        "stock": 10
    },
    {
        "id": 2,
        "name": "HP EliteBook 830 i5",
        "description": "Compact business laptop with Intel Core i5, perfect for professionals on the go. Lightweight design with excellent performance.",
        "price": 400000,
        "category": "Laptops",
        "image": "HP EliteBook 830 i5 ; 400,000 RWF.jpg",
        "stock": 8
    },
    {
        "id": 3,
        "name": "HP Envy X360 i7",
        "description": "2-in-1 convertible laptop with Intel Core i7, touchscreen display, versatile design. Transform from laptop to tablet mode effortlessly.",
        "price": 1200000,
        "category": "Laptops",
        "image": "Hp envy X360 i7 ; 1,200,000 RWF.jpeg",
        "stock": 5
    },
    {
        "id": 4,
        "name": "HP 290 Desktop",
        "description": "Compact desktop computer, ideal for office and home use. Reliable performance for everyday computing tasks.",
        "price": 850000,
        "category": "Computers",
        "image": "HP-290 ; 850,000 RWF.jpg",
        "stock": 7
    },
    {
        "id": 5,
        "name": "EPSON L3250",
        "description": "EcoTank all-in-one printer with wireless connectivity, high-capacity ink tanks. Print, scan, and copy with cost-effective ink system.",
        "price": 280000,
        "category": "Printers",
        "image": "EPSON L3250 ; 280,000 RWF.jpg",
        "stock": 12
    },
    {
        "id": 6,
        "name": "Epson L3210",
        "description": "EcoTank printer with refillable ink system, cost-effective printing solution. Save money with refillable ink tanks.",
        "price": 250000,
        "category": "Printers",
        "image": "Epson-L3210 ; 250,000 RWF.png",
        "stock": 15
    },
    {
        "id": 7,
        "name": "Canon ImageRunner 2224if",
        "description": "Multifunction printer with copy, scan, fax capabilities, network ready. Perfect for small to medium offices.",
        "price": 700000,
        "category": "Printers",
        "image": "imagerunner-2224if ; 700,000 Rwf.avif",
        "stock": 6
    },
    {
        "id": 8,
        "name": "XPRINTER 80",
        "description": "Compact thermal printer, perfect for receipts and labels. Ideal for retail and small businesses.",
        "price": 85000,
        "category": "Printers",
        "image": "XPRINTER 80 ; 85,000 RWF.jpg",
        "stock": 20
    },
    {
        "id": 9,
        "name": "SSD 512GB",
        "description": "High-speed 512GB solid state drive, upgrade your computer's performance. Dramatically faster than traditional hard drives.",
        "price": 55000,
        "category": "Storage",
        "image": "SSD 512 ; 55,000 RWF.jpeg",
        "stock": 25
    },
    {
        "id": 10,
        "name": "Flash Drive 64GB",
        "description": "Portable USB flash drive with 64GB storage capacity. Perfect for transferring files and backing up data.",
        "price": 20000,
        "category": "Storage",
        "image": "FLASH 64G ; 20,000 RWF.webp",
        "stock": 30
    },
    {
        "id": 11,
        "name": "CAT6 SFTP Cable",
        "description": "Shielded twisted pair network cable, high-speed data transmission. Perfect for reliable network connections.",
        "price": 110000,
        "category": "Networking",
        "image": "CAT6-SFTP ; 110,000 RWF.avif",
        "stock": 18
    },
    {
        "id": 12,
        "name": "UTP CAT6 Cable",
        "description": "Unshielded twisted pair network cable, reliable Ethernet connection. Standard network cable for home and office.",
        "price": 65000,
        "category": "Networking",
        "image": "UTP CAT6 ; 65,000 RWF.jpg",
        "stock": 22
    },
    {
        "id": 13,
        "name": "APC SMART UPS 750V",
        "description": "Uninterruptible power supply with 750VA capacity, protects your equipment from power surges and outages.",
        "price": 900000,
        "category": "Power",
        "image": "APC SMART 750V ; 900,000 RWF",
        "stock": 4
    }
]

categories_data = ["Laptops", "Computers", "Printers", "Storage", "Networking", "Power"]

def import_data():
    """Import categories and products into database"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        
        cursor = connection.cursor()
        
        print("=" * 60)
        print("Importing Categories and Products")
        print("=" * 60)
        
        # Import Categories
        print("\n1. Importing Categories...")
        category_map = {}
        for category_name in categories_data:
            # Check if category exists
            cursor.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
            existing = cursor.fetchone()
            
            if existing:
                category_map[category_name] = existing[0]
                print(f"   [OK] Category '{category_name}' already exists (ID: {existing[0]})")
            else:
                cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
                category_id = cursor.lastrowid
                category_map[category_name] = category_id
                print(f"   [OK] Created category '{category_name}' (ID: {category_id})")
        
        # Import Products
        print("\n2. Importing Products...")
        for product in products_data:
            category_id = category_map.get(product['category'])
            if not category_id:
                print(f"   [ERROR] Category '{product['category']}' not found for product '{product['name']}'")
                continue
            
            # Check if product exists
            cursor.execute("SELECT id FROM products WHERE name = %s", (product['name'],))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing product
                cursor.execute("""
                    UPDATE products 
                    SET price = %s, description = %s, category_id = %s, image = %s, stock = %s
                    WHERE id = %s
                """, (
                    product['price'],
                    product['description'],
                    category_id,
                    f"products/{product['image']}",
                    product['stock'],
                    existing[0]
                ))
                print(f"   [OK] Updated product '{product['name']}' (ID: {existing[0]})")
            else:
                # Insert new product
                cursor.execute("""
                    INSERT INTO products (name, price, description, category_id, image, stock)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    product['name'],
                    product['price'],
                    product['description'],
                    category_id,
                    f"products/{product['image']}",
                    product['stock']
                ))
                print(f"   [OK] Created product '{product['name']}' (ID: {cursor.lastrowid})")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        print("Import completed successfully!")
        print("=" * 60)
        
    except mysql.connector.Error as e:
        print(f"\n[ERROR] Database Error: {e}")
        print("Please check your database configuration in config.py")
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")

if __name__ == "__main__":
    import_data()

