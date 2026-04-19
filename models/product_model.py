"""
Product Model - Handles all product-related database operations
"""
import mysql.connector
from mysql.connector import Error
from config import Config

class ProductModel:
    """Product database operations"""
    
    @staticmethod
    def get_connection():
        """Create and return database connection"""
        try:
            connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def get_all_products(category_id=None, search=None, trending_only=False):
        """Get all products with optional filters"""
        connection = ProductModel.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT p.*, c.name as category_name,
                COALESCE(AVG(r.rating), 0) as avg_rating,
                COUNT(r.id) as review_count
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                LEFT JOIN reviews r ON p.id = r.product_id
            """
            conditions = []
            params = []
            
            if category_id:
                conditions.append("p.category_id = %s")
                params.append(category_id)
            
            if search:
                conditions.append("(p.name LIKE %s OR p.description LIKE %s)")
                params.extend([f"%{search}%", f"%{search}%"])
            
            if trending_only:
                conditions.append("p.trending = 1")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " GROUP BY p.id ORDER BY p.created_at DESC"
            cursor.execute(query, params)
            products = cursor.fetchall()
            cursor.close()
            connection.close()
            return products
        except Error as e:
            print(f"Error getting products: {e}")
            cursor.close()
            connection.close()
            return []
    
    @staticmethod
    def get_product_by_id(product_id):
        """Get product by ID with reviews"""
        connection = ProductModel.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT p.*, c.name as category_name,
                COALESCE(AVG(r.rating), 0) as avg_rating,
                COUNT(r.id) as review_count
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                LEFT JOIN reviews r ON p.id = r.product_id
                WHERE p.id = %s
                GROUP BY p.id
            """
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
            cursor.close()
            connection.close()
            return product
        except Error as e:
            print(f"Error getting product: {e}")
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def create_product(name, price, description, category_id, image, stock, trending=False):
        """Create a new product"""
        connection = ProductModel.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO products (name, price, description, category_id, image, stock, trending)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, price, description, category_id, image, stock, trending))
            connection.commit()
            product_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return product_id
        except Error as e:
            print(f"Error creating product: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def update_product(product_id, name=None, price=None, description=None, 
                       category_id=None, image=None, stock=None, trending=None):
        """Update product"""
        connection = ProductModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            updates = []
            values = []
            
            if name is not None:
                updates.append("name = %s")
                values.append(name)
            if price is not None:
                updates.append("price = %s")
                values.append(price)
            if description is not None:
                updates.append("description = %s")
                values.append(description)
            if category_id is not None:
                updates.append("category_id = %s")
                values.append(category_id)
            if image is not None:
                updates.append("image = %s")
                values.append(image)
            if stock is not None:
                updates.append("stock = %s")
                values.append(stock)
            if trending is not None:
                updates.append("trending = %s")
                values.append(trending)
            
            if not updates:
                return False
            
            values.append(product_id)
            query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error updating product: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def delete_product(product_id):
        """Delete product"""
        connection = ProductModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "DELETE FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error deleting product: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def reduce_stock(product_id, quantity):
        """Reduce product stock"""
        connection = ProductModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "UPDATE products SET stock = stock - %s WHERE id = %s AND stock >= %s"
            cursor.execute(query, (quantity, product_id, quantity))
            connection.commit()
            success = cursor.rowcount > 0
            cursor.close()
            connection.close()
            return success
        except Error as e:
            print(f"Error reducing stock: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def get_all_categories():
        """Get all categories"""
        connection = ProductModel.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM categories ORDER BY name"
            cursor.execute(query)
            categories = cursor.fetchall()
            cursor.close()
            connection.close()
            return categories
        except Error as e:
            print(f"Error getting categories: {e}")
            cursor.close()
            connection.close()
            return []
    
    @staticmethod
    def create_category(name):
        """Create a new category"""
        connection = ProductModel.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            query = "INSERT INTO categories (name) VALUES (%s)"
            cursor.execute(query, (name,))
            connection.commit()
            category_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return category_id
        except Error as e:
            print(f"Error creating category: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def get_similar_products(product_id, category_id, limit=4):
        """Get similar products by category"""
        connection = ProductModel.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT p.*, c.name as category_name,
                COALESCE(AVG(r.rating), 0) as avg_rating
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                LEFT JOIN reviews r ON p.id = r.product_id
                WHERE p.category_id = %s AND p.id != %s AND p.stock > 0
                GROUP BY p.id
                ORDER BY p.created_at DESC
                LIMIT %s
            """
            cursor.execute(query, (category_id, product_id, limit))
            products = cursor.fetchall()
            cursor.close()
            connection.close()
            return products
        except Error as e:
            print(f"Error getting similar products: {e}")
            cursor.close()
            connection.close()
            return []



