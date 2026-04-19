"""
Main Flask Application - E-commerce Platform
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file, flash
from functools import wraps
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import bcrypt

from config import Config
from models.user_model import UserModel
from models.product_model import ProductModel
from models.cart_model import CartModel
from models.order_model import OrderModel
from models.settings_model import SettingsModel
from utils.helpers import save_uploaded_file, save_uploaded_video, format_currency, calculate_tax, calculate_total
from utils.pdf_generator import generate_invoice

app = Flask(__name__)
app.config.from_object(Config)

# Make config available to all templates
@app.context_processor
def inject_config():
    return dict(config=Config)

# Ensure upload directories exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.VIDEO_UPLOAD_FOLDER, exist_ok=True)

# ==================== DECORATORS ====================

def login_required(f):
    """Decorator to require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== HELPER FUNCTIONS ====================

def get_db_connection():
    """Get database connection"""
    try:
        return mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def get_cart_count():
    """Get cart item count for current user"""
    if 'user_id' in session:
        return CartModel.get_cart_count(session['user_id'])
    return 0

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def home():
    """Home page - display products"""
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    trending = request.args.get('trending', type=bool)
    view_all = request.args.get('view_all', type=bool)
    
    products = ProductModel.get_all_products(
        category_id=category_id,
        search=search,
        trending_only=trending
    )
    
    total_products = len(products)
    
    # Limit to 8 products initially unless view_all is True or category/search is active
    if not view_all and not search and not category_id:
        products = products[:8]
    
    categories = ProductModel.get_all_categories()
    cart_count = get_cart_count()
    home_video = SettingsModel.get_setting('home_video')
    
    return render_template('home.html', 
                         products=products, 
                         categories=categories,
                         cart_count=cart_count,
                         search=search,
                         selected_category=category_id,
                         view_all=view_all,
                         total_products=total_products,
                         home_video=home_video)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        address = request.form.get('address')
        
        if not all([name, email, phone, password]):
            flash('Please fill all required fields', 'error')
            return render_template('auth/signup.html')
        
        # Check if user exists
        existing_user = UserModel.get_user_by_email(email)
        if existing_user:
            flash('Email already registered. Please login.', 'error')
            return render_template('auth/signup.html')
        
        user_id = UserModel.create_user(name, email, phone, password, address)
        if user_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('auth/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserModel.authenticate_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        if UserModel.update_user(session['user_id'], name, phone, address):
            flash('Profile updated successfully', 'success')
            session['user_name'] = name
            return redirect(url_for('profile'))
        else:
            flash('Failed to update profile', 'error')
    
    user = UserModel.get_user_by_id(session['user_id'])
    cart_count = get_cart_count()
    return render_template('user/profile.html', user=user, cart_count=cart_count)

# ==================== PRODUCT ROUTES ====================

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = ProductModel.get_product_by_id(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('home'))
    
    # Get reviews
    connection = get_db_connection()
    reviews = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT r.*, u.name as user_name
                FROM reviews r
                JOIN users u ON r.user_id = u.id
                WHERE r.product_id = %s
                ORDER BY r.created_at DESC
            """
            cursor.execute(query, (product_id,))
            reviews = cursor.fetchall()
            cursor.close()
        except Error as e:
            print(f"Error getting reviews: {e}")
        finally:
            connection.close()
    
    # Get similar products
    similar_products = ProductModel.get_similar_products(
        product_id, 
        product['category_id'] if product['category_id'] else 0
    )
    
    cart_count = get_cart_count()
    return render_template('product.html', 
                         product=product, 
                         reviews=reviews,
                         similar_products=similar_products,
                         cart_count=cart_count)

@app.route('/add_review', methods=['POST'])
@login_required
def add_review():
    """Add product review"""
    product_id = request.form.get('product_id', type=int)
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '')
    
    if not product_id or not rating or rating < 1 or rating > 5:
        return jsonify({'success': False, 'message': 'Invalid review data'})
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database error'})
    
    try:
        cursor = connection.cursor()
        # Check if user already reviewed
        check_query = "SELECT id FROM reviews WHERE product_id = %s AND user_id = %s"
        cursor.execute(check_query, (product_id, session['user_id']))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing review
            update_query = "UPDATE reviews SET rating = %s, comment = %s WHERE id = %s"
            cursor.execute(update_query, (rating, comment, existing[0]))
        else:
            # Insert new review
            insert_query = "INSERT INTO reviews (product_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (product_id, session['user_id'], rating, comment))
        
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'success': True, 'message': 'Review submitted successfully'})
    except Error as e:
        print(f"Error adding review: {e}")
        connection.rollback()
        cursor.close()
        connection.close()
        return jsonify({'success': False, 'message': 'Failed to submit review'})

# ==================== CART ROUTES ====================

@app.route('/cart')
def cart():
    """Shopping cart page - requires login to proceed to checkout"""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to view your cart and place orders', 'error')
        return redirect(url_for('login'))
    
    # User is logged in, show cart
    """Shopping cart page"""
    from decimal import Decimal
    items = CartModel.get_cart_items(session['user_id'])
    # Ensure Decimal handling for price calculations
    subtotal = sum(Decimal(str(item['price'])) * Decimal(str(item['quantity'])) for item in items)
    # No tax, delivery fee calculated at checkout
    total = subtotal
    cart_count = get_cart_count()
    
    return render_template('cart.html', 
                         items=items, 
                         subtotal=subtotal,
                         total=total,
                         cart_count=cart_count)

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    """Add item to cart"""
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not product_id:
        return jsonify({'success': False, 'message': 'Invalid product'})
    
    # Check stock
    product = ProductModel.get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'})
    
    if product['stock'] < quantity:
        return jsonify({'success': False, 'message': 'Not enough stock available'})
    
    # Check current cart quantity
    cart_items = CartModel.get_cart_items(session['user_id'])
    current_quantity = sum(item['quantity'] for item in cart_items if item['product_id'] == product_id)
    
    if current_quantity + quantity > product['stock']:
        return jsonify({'success': False, 'message': 'Not enough stock available'})
    
    if CartModel.add_to_cart(session['user_id'], product_id, quantity):
        cart_count = CartModel.get_cart_count(session['user_id'])
        return jsonify({'success': True, 'message': 'Item added to cart', 'cart_count': cart_count})
    else:
        return jsonify({'success': False, 'message': 'Failed to add to cart'})

@app.route('/update_cart', methods=['POST'])
@login_required
def update_cart():
    """Update cart item quantity"""
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    if not product_id or quantity < 1:
        return jsonify({'success': False, 'message': 'Invalid data'})
    
    # Check stock
    product = ProductModel.get_product_by_id(product_id)
    if not product or product['stock'] < quantity:
        return jsonify({'success': False, 'message': 'Not enough stock'})
    
    if CartModel.update_cart_item(session['user_id'], product_id, quantity):
        return jsonify({'success': True, 'message': 'Cart updated'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update cart'})

@app.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    """Remove item from cart"""
    product_id = request.form.get('product_id', type=int)
    
    if CartModel.remove_from_cart(session['user_id'], product_id):
        return jsonify({'success': True, 'message': 'Item removed from cart'})
    else:
        return jsonify({'success': False, 'message': 'Failed to remove item'})

# ==================== CHECKOUT ROUTES ====================

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    if request.method == 'POST':
        shipping_name = request.form.get('name')
        shipping_phone = request.form.get('phone')
        shipping_address = request.form.get('address')
        payment_method = request.form.get('payment_method')
        
        if not all([shipping_name, shipping_phone, shipping_address, payment_method]):
            flash('Please fill all required fields', 'error')
            return redirect(url_for('checkout'))
        
        # Get cart items
        cart_items = CartModel.get_cart_items(session['user_id'])
        if not cart_items:
            flash('Your cart is empty', 'error')
            return redirect(url_for('cart'))
        
        # Validate stock
        for item in cart_items:
            product = ProductModel.get_product_by_id(item['product_id'])
            if not product or product['stock'] < item['quantity']:
                flash(f'Insufficient stock for {item["name"]}', 'error')
                return redirect(url_for('cart'))
        
        # Calculate total
        from decimal import Decimal
        subtotal = sum(Decimal(str(item['price'])) * Decimal(str(item['quantity'])) for item in cart_items)
        
        # Get delivery location and fee
        delivery_location = request.form.get('location')
        if delivery_location == 'kigali':
            delivery_fee = Decimal('1500')
        elif delivery_location == 'outside':
            delivery_fee = Decimal('2000')
        else:
            delivery_fee = Decimal('0')
        
        total = subtotal + delivery_fee
        
        # Create order
        order_id = OrderModel.create_order(
            session['user_id'],
            total,
            payment_method,
            shipping_name,
            shipping_phone,
            shipping_address,
            cart_items
        )
        
        if order_id:
            # Reduce stock
            for item in cart_items:
                ProductModel.reduce_stock(item['product_id'], item['quantity'])
            
            # Clear cart
            CartModel.clear_cart(session['user_id'])
            
            flash('Order placed successfully!', 'success')
            return redirect(url_for('order_success', order_id=order_id))
        else:
            flash('Failed to place order. Please try again.', 'error')
    
    # GET request - show checkout form
    cart_items = CartModel.get_cart_items(session['user_id'])
    if not cart_items:
        flash('Your cart is empty', 'error')
        return redirect(url_for('cart'))
    
    from decimal import Decimal
    subtotal = sum(Decimal(str(item['price'])) * Decimal(str(item['quantity'])) for item in cart_items)
    # Total will be calculated with delivery fee in template
    total = subtotal
    
    user = UserModel.get_user_by_id(session['user_id'])
    cart_count = get_cart_count()
    
    return render_template('checkout.html',
                         items=cart_items,
                         subtotal=subtotal,
                         total=total,
                         user=user,
                         cart_count=cart_count)

@app.route('/order_success/<int:order_id>')
@login_required
def order_success(order_id):
    """Order success page"""
    order = OrderModel.get_order_by_id(order_id)
    if not order or order['user_id'] != session['user_id']:
        flash('Order not found', 'error')
        return redirect(url_for('home'))
    
    cart_count = get_cart_count()
    return render_template('user/order_success.html', order=order, cart_count=cart_count)

# ==================== ORDER ROUTES ====================

@app.route('/orders')
@login_required
def orders():
    """User order history"""
    user_orders = OrderModel.get_user_orders(session['user_id'])
    cart_count = get_cart_count()
    return render_template('user/orders.html', orders=user_orders, cart_count=cart_count)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """Order detail page"""
    from decimal import Decimal
    
    order = OrderModel.get_order_by_id(order_id)
    if not order or order['user_id'] != session['user_id']:
        flash('Order not found', 'error')
        return redirect(url_for('orders'))
    
    # Calculate subtotal (no tax, delivery fee included in total)
    total = Decimal(str(order['total']))
    # For display, we'll show the total as subtotal since tax is removed
    # Delivery fee is already included in the total
    subtotal = total
    
    cart_count = get_cart_count()
    return render_template('user/order_detail.html', 
                         order=order, 
                         cart_count=cart_count,
                         subtotal=float(subtotal),
                         total=float(total))

@app.route('/download_invoice/<int:order_id>')
@login_required
def download_invoice(order_id):
    """Download order invoice PDF"""
    order = OrderModel.get_order_by_id(order_id)
    if not order or order['user_id'] != session['user_id']:
        flash('Order not found', 'error')
        return redirect(url_for('orders'))
    
    # Generate PDF
    output_path = f"static/invoices/invoice_{order_id}.pdf"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    generate_invoice(order, order['items'], output_path)
    
    return send_file(output_path, as_attachment=True, download_name=f"invoice_{order['order_number']}.pdf")

# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM admin WHERE email = %s"
                cursor.execute(query, (email,))
                admin = cursor.fetchone()
                cursor.close()
                connection.close()
                
                if admin and bcrypt.checkpw(password.encode('utf-8'), admin['password'].encode('utf-8')):
                    session['admin_id'] = admin['id']
                    session['admin_email'] = admin['email']
                    flash('Admin login successful!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid credentials', 'error')
            except Error as e:
                print(f"Error: {e}")
                flash('Login failed', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_id', None)
    session.pop('admin_email', None)
    flash('Admin logged out', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    stats = OrderModel.get_order_stats()
    
    # Get total users
    connection = get_db_connection()
    total_users = 0
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM users")
            total_users = cursor.fetchone()[0]
            cursor.close()
        except Error as e:
            print(f"Error: {e}")
        finally:
            connection.close()
    
    stats['total_users'] = total_users
    
    return render_template('admin/dashboard.html', stats=stats, cart_count=0)

@app.route('/admin/products')
@admin_required
def admin_products():
    """Admin product management"""
    products = ProductModel.get_all_products()
    categories = ProductModel.get_all_categories()
    return render_template('admin/products.html', products=products, categories=categories, cart_count=0)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product"""
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price', type=float)
        description = request.form.get('description')
        category_id = request.form.get('category_id', type=int)
        stock = request.form.get('stock', type=int)
        trending = request.form.get('trending') == 'on'
        
        # Handle image upload
        image_file = request.files.get('image')
        image_path = None
        if image_file and image_file.filename:
            image_path = save_uploaded_file(image_file)
        
        if not all([name, price, category_id]):
            flash('Please fill all required fields', 'error')
            return redirect(url_for('admin_add_product'))
        
        product_id = ProductModel.create_product(
            name, price, description, category_id, image_path, stock, trending
        )
        
        if product_id:
            flash('Product added successfully', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash('Failed to add product', 'error')
    
    categories = ProductModel.get_all_categories()
    return render_template('admin/add_product.html', categories=categories, cart_count=0)

@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit product"""
    product = ProductModel.get_product_by_id(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('admin_products'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price', type=float)
        description = request.form.get('description')
        category_id = request.form.get('category_id', type=int)
        stock = request.form.get('stock', type=int)
        trending = request.form.get('trending') == 'on'
        
        # Handle image upload
        image_file = request.files.get('image')
        image_path = product['image']  # Keep existing if no new image
        if image_file and image_file.filename:
            image_path = save_uploaded_file(image_file)
        
        if ProductModel.update_product(
            product_id, name, price, description, category_id, image_path, stock, trending
        ):
            flash('Product updated successfully', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash('Failed to update product', 'error')
    
    categories = ProductModel.get_all_categories()
    return render_template('admin/edit_product.html', product=product, categories=categories, cart_count=0)

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Delete product"""
    if ProductModel.delete_product(product_id):
        flash('Product deleted successfully', 'success')
    else:
        flash('Failed to delete product', 'error')
    return redirect(url_for('admin_products'))

@app.route('/admin/categories', methods=['GET', 'POST'])
@admin_required
def admin_categories():
    """Manage categories"""
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            ProductModel.create_category(name)
            flash('Category added successfully', 'success')
    
    categories = ProductModel.get_all_categories()
    return render_template('admin/categories.html', categories=categories, cart_count=0)

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Admin order management"""
    orders = OrderModel.get_all_orders()
    return render_template('admin/orders.html', orders=orders, cart_count=0)

@app.route('/admin/order/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    """Admin order detail"""
    order = OrderModel.get_order_by_id(order_id)
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('admin_orders'))
    return render_template('admin/order_detail.html', order=order, cart_count=0)

@app.route('/admin/order/update_status', methods=['POST'])
@admin_required
def admin_update_order_status():
    """Update order status"""
    order_id = request.form.get('order_id', type=int)
    status = request.form.get('status')
    
    if OrderModel.update_order_status(order_id, status):
        flash('Order status updated successfully', 'success')
    else:
        flash('Failed to update order status', 'error')
    
    return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route('/admin/video', methods=['GET', 'POST'])
@admin_required
def admin_video():
    """Admin video management"""
    if request.method == 'POST':
        # Check if delete button was clicked
        if 'delete' in request.form:
            # Delete video
            old_video = SettingsModel.get_setting('home_video')
            if old_video:
                old_path = os.path.join(Config.VIDEO_UPLOAD_FOLDER, old_video)
                if os.path.exists(old_path):
                    os.remove(old_path)
                SettingsModel.set_setting('home_video', '')
                flash('Video deleted successfully!', 'success')
            else:
                flash('No video to delete', 'error')
        elif 'video' in request.files:
            video_file = request.files['video']
            if video_file and video_file.filename:
                # Delete old video if exists
                old_video = SettingsModel.get_setting('home_video')
                if old_video:
                    old_path = os.path.join(Config.VIDEO_UPLOAD_FOLDER, old_video)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                # Save new video
                filename = save_uploaded_video(video_file)
                if filename:
                    SettingsModel.set_setting('home_video', filename)
                    flash('Video uploaded successfully!', 'success')
                else:
                    flash('Invalid video file. Allowed formats: mp4, webm, ogg, mov', 'error')
            else:
                flash('No video file selected', 'error')
        return redirect(url_for('admin_video'))
    
    current_video = SettingsModel.get_setting('home_video')
    return render_template('admin/video.html', current_video=current_video, cart_count=0)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

