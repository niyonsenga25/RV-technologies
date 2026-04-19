"""
Settings Model - Handles site settings including video
"""
import mysql.connector
from mysql.connector import Error
from config import Config

class SettingsModel:
    """Site settings database operations"""
    
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
    def get_setting(key, default=None):
        """Get a setting value by key"""
        connection = SettingsModel.get_connection()
        if not connection:
            return default
        
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT setting_value FROM site_settings WHERE setting_key = %s"
            cursor.execute(query, (key,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result:
                return result['setting_value'] if result['setting_value'] else default
            return default
        except Error as e:
            print(f"Error getting setting: {e}")
            cursor.close()
            connection.close()
            return default
    
    @staticmethod
    def set_setting(key, value):
        """Set a setting value by key"""
        connection = SettingsModel.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO site_settings (setting_key, setting_value) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE setting_value = %s
            """
            cursor.execute(query, (key, value, value))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error setting setting: {e}")
            connection.rollback()
            cursor.close()
            connection.close()
            return False


