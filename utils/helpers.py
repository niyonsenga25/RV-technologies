"""
Helper utility functions
"""
import os
from decimal import Decimal
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    """Check if video file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_VIDEO_EXTENSIONS

def save_uploaded_file(file, folder='products'):
    """Save uploaded file and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        import time
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        upload_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        return f"products/{filename}"
    return None

def save_uploaded_video(file):
    """Save uploaded video file and return filename"""
    if file and allowed_video_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        import time
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        upload_path = os.path.join(Config.VIDEO_UPLOAD_FOLDER, filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)
        return filename
    return None

def format_currency(amount):
    """Format amount as currency"""
    # Handle Decimal types
    if isinstance(amount, Decimal):
        return f"{float(amount):,.0f} RWF"
    return f"{amount:,.0f} RWF"

def calculate_tax(subtotal, tax_rate=0.18):
    """Calculate tax (18% VAT)"""
    # Convert to Decimal for consistent calculations
    if isinstance(subtotal, Decimal):
        return subtotal * Decimal(str(tax_rate))
    else:
        return Decimal(str(subtotal)) * Decimal(str(tax_rate))

def calculate_total(subtotal, tax):
    """Calculate total with tax"""
    # Convert to Decimal for consistent calculations
    if isinstance(subtotal, Decimal):
        subtotal_decimal = subtotal
    else:
        subtotal_decimal = Decimal(str(subtotal))
    
    if isinstance(tax, Decimal):
        tax_decimal = tax
    else:
        tax_decimal = Decimal(str(tax))
    
    return subtotal_decimal + tax_decimal

