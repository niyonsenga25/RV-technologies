"""
Order Model - Handles order-related database operations
"""
import mysql.connector
from mysql.connector import Error
import random
import string
from datetime import datetime
from config import Config

class OrderModel:
    """Order database operations"""
    
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
    def generate_order_number():
        """Generate unique order number"""
        timestamp = datetime.now().strftime("%Y%m%d")
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"ORD-{timestamp}-{random_str}"
    
    @staticmethod
    def create_order(user_id, total, payment_method, shipping_name, shipping_phone, shipping_address, cart_items):
        """Create a new order with order items"""
        connection = OrderModel.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            order_number = OrderModel.generate_order_number()
            
            # Create order
            order_query = """
                INSERT INTO orders (user_id, total, payment_method, shipping_name, shipping_phone, shipping_address, order_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(order_query, (user_id, total, payment_method, shipping_name, shipping_phone, shipping_address, order_number))
            order_id = cursor.lastrowid
            
            # Create order items
            for item in cart_items:
                item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(item_query, (order_id, item['product_id'], item['quantity'], item['price']))
            
            connection.commit()
            cursor.close()
            connection.close()
            return order_id
        except Error as e:
            print(f"Error creating order: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def get_order_by_id(order_id):
        """Get order by ID with items"""
        connection = OrderModel.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            # Get order
            order_query = """
                SELECT o.*, u.name as user_name, u.email as user_email
                FROM orders o
                JOIN users u ON o.user_id = u.id
                WHERE o.id = %s
            """
            cursor.execute(order_query, (order_id,))
            order = cursor.fetchone()
            
            if order:
                # Get order items
                items_query = """
                    SELECT oi.*, p.name as product_name, p.image
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """
                cursor.execute(items_query, (order_id,))
                items = cursor.fetchall()
                order['items'] = items if items else []
            else:
                return None
            
            cursor.close()
            connection.close()
            return order
        except Error as e:
            print(f"Error getting order: {e}")
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def get_user_orders(user_id):
        """Get all orders for a user"""
        connection = OrderModel.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT o.*, 
                (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
                FROM orders o
                WHERE o.user_id = %s
                ORDER BY o.created_at DESC
            """
            cursor.execute(query, (user_id,))
            orders = cursor.fetchall()
            cursor.close()
            connection.close()
            return orders
        except Error as e:
            print(f"Error getting user orders: {e}")
            cursor.close()
            connection.close()
            return []
    
    @staticmethod
    def get_all_orders():
        """Get all orders (admin)"""
        connection = OrderModel.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT o.*, u.name as user_name, u.email as user_email,
                (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
                FROM orders o
                JOIN users u ON o.user_id = u.id
                ORDER BY o.created_at DESC
            """
            cursor.execute(query)
            orders = cursor.fetchall()
            cursor.close()
            connection.close()
            return orders
        except Error as e:
            print(f"Error getting all orders: {e}")
            cursor.close()
            connection.close()
            return []
    
    @staticmethod
    def update_order_status(order_id, status):
        """Update order status"""
        connection = OrderModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = "UPDATE orders SET status = %s WHERE id = %s"
            cursor.execute(query, (status, order_id))
            connection.commit()
            success = cursor.rowcount > 0
            cursor.close()
            connection.close()
            return success
        except Error as e:
            print(f"Error updating order status: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def get_order_stats():
        """Get order statistics for admin dashboard"""
        connection = OrderModel.get_connection()
        if not connection:
            return {}
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Total sales
            cursor.execute("SELECT SUM(total) as total_sales FROM orders WHERE status != 'Cancelled'")
            total_sales = cursor.fetchone()['total_sales'] or 0
            
            # Total orders
            cursor.execute("SELECT COUNT(*) as total_orders FROM orders")
            total_orders = cursor.fetchone()['total_orders']
            
            # Pending orders
            cursor.execute("SELECT COUNT(*) as pending_orders FROM orders WHERE status = 'Pending'")
            pending_orders = cursor.fetchone()['pending_orders']
            
            # Best selling products
            cursor.execute("""
                SELECT p.id, p.name, p.image, SUM(oi.quantity) as total_sold, SUM(oi.quantity * oi.price) as revenue
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                JOIN orders o ON oi.order_id = o.id
                WHERE o.status != 'Cancelled'
                GROUP BY p.id, p.name, p.image
                ORDER BY total_sold DESC
                LIMIT 5
            """)
            best_sellers = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return {
                'total_sales': float(total_sales),
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'best_sellers': best_sellers
            }
        except Error as e:
            print(f"Error getting order stats: {e}")
            cursor.close()
            connection.close()
            return {}



