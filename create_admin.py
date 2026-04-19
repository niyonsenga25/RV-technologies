"""
Quick script to create admin account
"""
import bcrypt
import mysql.connector
from config import Config

def create_admin():
    """Create admin account with default credentials"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        
        cursor = connection.cursor()
        
        email = "admin@example.com"
        password = "admin123"
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Check if admin exists
        check_query = "SELECT id FROM admin WHERE email = %s"
        cursor.execute(check_query, (email,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing admin
            update_query = "UPDATE admin SET password = %s WHERE email = %s"
            cursor.execute(update_query, (hashed_password, email))
            print("Admin account password updated successfully!")
        else:
            # Create new admin
            insert_query = "INSERT INTO admin (email, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (email, hashed_password))
            print("Admin account created successfully!")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"\nAdmin Email: {email}")
        print(f"Admin Password: {password}")
        print("\nYou can now login with these credentials!")
        
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
        print("\nPlease check:")
        print("1. MySQL is running")
        print("2. Database 'ecommerce_db' exists")
        print("3. Database credentials in config.py are correct")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_admin()



