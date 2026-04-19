"""
User Model - Handles all user-related database operations
"""
import mysql.connector
from mysql.connector import Error
import bcrypt
from config import Config

class UserModel:
    """User database operations"""
    
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
    def hash_password(password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def create_user(name, email, phone, password, address=None):
        """Create a new user"""
        connection = UserModel.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            hashed_password = UserModel.hash_password(password)
            
            query = """
                INSERT INTO users (name, email, phone, password, address)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, phone, hashed_password, address))
            connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return user_id
        except Error as e:
            print(f"Error creating user: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        connection = UserModel.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        connection = UserModel.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id, name, email, phone, address, created_at FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        except Error as e:
            print(f"Error getting user: {e}")
            cursor.close()
            connection.close()
            return None
    
    @staticmethod
    def update_user(user_id, name=None, phone=None, address=None):
        """Update user profile"""
        connection = UserModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            updates = []
            values = []
            
            if name:
                updates.append("name = %s")
                values.append(name)
            if phone:
                updates.append("phone = %s")
                values.append(phone)
            if address:
                updates.append("address = %s")
                values.append(address)
            
            if not updates:
                return False
            
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error updating user: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user login"""
        user = UserModel.get_user_by_email(email)
        if not user:
            return None
        
        if UserModel.verify_password(password, user['password']):
            return {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'address': user['address']
            }
        return None



