"""
Script to set up or update admin account
Run this script to create/update admin credentials
"""
import bcrypt
import mysql.connector
from config import Config

def setup_admin():
    """Create or update admin account"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        
        cursor = connection.cursor()
        
        print("=" * 50)
        print("Admin Account Setup")
        print("=" * 50)
        
        email = input("Enter admin email (default: admin@example.com): ").strip()
        if not email:
            email = "admin@example.com"
        
        password = input("Enter admin password (default: admin123): ").strip()
        if not password:
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
            print(f"\n✓ Admin account updated successfully!")
        else:
            # Create new admin
            insert_query = "INSERT INTO admin (email, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (email, hashed_password))
            print(f"\n✓ Admin account created successfully!")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"\nAdmin Email: {email}")
        print(f"Admin Password: {password}")
        print("\n⚠️  Please save these credentials securely!")
        print("=" * 50)
        
    except mysql.connector.Error as e:
        print(f"\n✗ Error: {e}")
        print("Please check your database configuration in config.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    setup_admin()



