# Quick Setup Guide

## Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] MySQL 5.7+ or 8.0+ installed and running
- [ ] pip (Python package manager) installed

## Quick Start (5 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create MySQL Database
```sql
CREATE DATABASE ecommerce_db;
```

### 3. Import Database Schema
```bash
mysql -u root -p ecommerce_db < database/schema.sql
```

### 4. Configure Database
Edit `config.py` or set environment variables:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DATABASE = 'ecommerce_db'
```

### 5. Run the Application
```bash
python app.py
```

Visit: `http://localhost:5000`

## Default Admin Credentials
- **Email**: admin@example.com
- **Password**: admin123

⚠️ **Change the admin password immediately!**

To change admin password, run:
```bash
python setup_admin.py
```

## First Steps After Setup

1. **Login as Admin** (`/admin/login`)
   - Add product categories
   - Add products with images
   - View dashboard

2. **Create User Account** (`/signup`)
   - Browse products
   - Add items to cart
   - Place an order

3. **Test Features**
   - Search products
   - Filter by category
   - Add reviews
   - Download invoice

## Common Issues

### Database Connection Error
- Ensure MySQL is running
- Check credentials in `config.py`
- Verify database exists

### Image Upload Not Working
- Create directory: `mkdir -p static/images/products`
- Check file permissions
- Verify file size (max 16MB)

### Admin Login Fails
- Run `python setup_admin.py` to reset password
- Check database admin table
- Clear browser cookies

## Directory Structure
```
project/
├── app.py              # Main application
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── database/
│   └── schema.sql      # Database schema
├── models/             # Database models
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── utils/              # Utility functions
```

## Next Steps
- Add your products
- Customize design
- Configure email (optional)
- Deploy to production

For detailed documentation, see `README.md`



