"""
Cart Model - Handles shopping cart database operations
"""
import mysql.connector
from mysql.connector import Error
from config import Config

class CartModel:
    """Cart database operations"""
    
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
    def get_cart_items(user_id):
        """Get all cart items for a user"""
        connection = CartModel.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT c.*, p.name, p.price, p.image, p.stock
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
                ORDER BY c.created_at DESC
            """
            cursor.execute(query, (user_id,))
            items = cursor.fetchall()
            cursor.close()
            connection.close()
            return items
        except Error as e:
            print(f"Error getting cart items: {e}")
            cursor.close()
            connection.close()
            return []
    
    @staticmethod
    def add_to_cart(user_id, product_id, quantity=1):
        """Add item to cart or update quantity if exists"""
        connection = CartModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            # Check if item already exists
            check_query = "SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s"
            cursor.execute(check_query, (user_id, product_id))
            existing = cursor.fetchone()
            
            if existing:
                # Update quantity
                new_quantity = existing[1] + quantity
                update_query = "UPDATE cart SET quantity = %s WHERE id = %s"
                cursor.execute(update_query, (new_quantity, existing[0]))
            else:
                # Insert new item
                insert_query = "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (user_id, product_id, quantity))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error adding to cart: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def update_cart_item(user_id, product_id, quantity):
        """Update cart item quantity"""
        connection = CartModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s"
            cursor.execute(query, (quantity, user_id, product_id))
            connection.commit()
            success = cursor.rowcount > 0
            cursor.close()
            connection.close()
            return success
        except Error as e:
            print(f"Error updating cart item: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def remove_from_cart(user_id, product_id):
        """Remove item from cart"""
        connection = CartModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "DELETE FROM cart WHERE user_id = %s AND product_id = %s"
            cursor.execute(query, (user_id, product_id))
            connection.commit()
            success = cursor.rowcount > 0
            cursor.close()
            connection.close()
            return success
        except Error as e:
            print(f"Error removing from cart: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def clear_cart(user_id):
        """Clear all items from cart"""
        connection = CartModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "DELETE FROM cart WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error clearing cart: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def get_cart_total(user_id):
        """Calculate cart total"""
        items = CartModel.get_cart_items(user_id)
        total = sum(item['price'] * item['quantity'] for item in items)
        return total
    
    @staticmethod
    def get_cart_count(user_id):
        """Get total number of items in cart"""
        items = CartModel.get_cart_items(user_id)
        return sum(item['quantity'] for item in items)



