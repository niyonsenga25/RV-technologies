"""
Setup video support in database
"""
import mysql.connector
from config import Config

def setup_video_support():
    """Create site_settings table for video"""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        
        cursor = connection.cursor()
        
        # Create site_settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS site_settings (
                id INT PRIMARY KEY AUTO_INCREMENT,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Insert default video setting
        cursor.execute("""
            INSERT INTO site_settings (setting_key, setting_value) 
            VALUES ('home_video', '')
            ON DUPLICATE KEY UPDATE setting_key=setting_key
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("=" * 60)
        print("Video support setup completed successfully!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Go to Admin Dashboard")
        print("2. Click 'Manage Video'")
        print("3. Upload a video file (MP4, WebM, OGG, MOV)")
        print("4. The video will appear on the home page under 'Our Values'")
        
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
    setup_video_support()


