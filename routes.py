import random
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, flash
from app import app, db
from models import Product, RedemptionLink, UserDetails

# Initialize default products if none exist
# def init_products():
#     with app.app_context():
#         if Product.query.count() == 0:
#             default_products = [
#                 {
#                     'name': '$50 Apple Gift Card',
#                     'description': 'Redeem for apps, games, music, and more',
#                     'image_url': 'https://via.assets.so/img.jpg?w=300&h=200&tc=white&bg=%23007AFF&t=$50%20Apple%20Gift%20Card'
#                 },
#                 {
#                     'name': '$25 Amazon Voucher',
#                     'description': 'Shop millions of products on Amazon',
#                     'image_url': 'https://via.assets.so/img.jpg?w=300&h=200&tc=white&bg=%23FF9900&t=$25%20Amazon%20Voucher'
#                 },
#                 {
#                     'name': '$30 Spotify Premium',
#                     'description': '3 months of ad-free music streaming',
#                     'image_url': 'https://via.assets.so/img.jpg?w=300&h=200&tc=white&bg=%231DB954&t=$30%20Spotify%20Premium'
#                 },
#                 {
#                     'name': '$20 Netflix Credit',
#                     'description': 'Watch your favorite shows and movies',
#                     'image_url': 'https://via.assets.so/img.jpg?w=300&h=200&tc=white&bg=%23E50914&t=$20%20Netflix%20Credit'
#                 },
#                 {
#                     'name': '$40 Gaming Bundle',
#                     'description': 'Steam credits and gaming accessories',
#                     'image_url': 'https://via.assets.so/img.jpg?w=300&h=200&tc=white&bg=%23171A21&t=$40%20Gaming%20Bundle'
#                 }
#             ]
            
#             for product_data in default_products:
#                 # Clean the product name for database storage
#                 clean_name = product_data['name'].replace('£', 'GBP').replace('$', 'USD')
#                 product_data['name'] = clean_name
#                 product = Product(**product_data)
#                 db.session.add(product)
            
#             db.session.commit()

@app.route('/')
def index():
    """Main scratch card page"""
    # Clear any existing session data
    session.pop('won_product_id', None)
    session.pop('redemption_token', None)
    return render_template('index.html')

@app.route('/scratch_result', methods=['POST'])
def scratch_result():
    """Handle scratch card result - assign random product to existing link"""
    redemption_token = session.get('redemption_token')
    
    if not redemption_token:
        flash('No valid redemption link found.', 'error')
        return render_template('500.html')
    
    # Find the redemption link
    redemption_link = RedemptionLink.query.filter_by(token=redemption_token).first()
    
    if not redemption_link or redemption_link.is_redeemed:
        flash('Invalid or already used redemption link.', 'error')
        return redirect(url_for('index'))
    
    # Get all products
    products = Product.query.all()
    if not products:
        flash('No products available at the moment.', 'error')
        return redirect(url_for('index'))
    
    # Select random product if not already assigned
    if not redemption_link.product_id:
        won_product = random.choice(products)
        redemption_link.product_id = won_product.id
        db.session.commit()
    
    # Store in session
    session['won_product_id'] = redemption_link.product_id
    
    return redirect(url_for('details'))

@app.route('/details', methods=['GET', 'POST'])
def details():
    """User details collection page"""
    # Check if user has a won product in session
    won_product_id = session.get('won_product_id')
    redemption_token = session.get('redemption_token')
    
    if not won_product_id or not redemption_token:
        pass
    
    won_product = Product.query.get(won_product_id)
    if not won_product:
        flash('Invalid product selection.', 'error')
        return render_template('500.html', product=won_product)
    
    if request.method == 'POST':
        # Validate form data
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        if not full_name or not email:
            flash('Full name and email are required.', 'error')
            return render_template('details.html', product=won_product)
        
        # Get redemption link
        redemption_link = RedemptionLink.query.filter_by(token=redemption_token).first()
        if not redemption_link:
            flash('Invalid redemption link.', 'error')
            return redirect(url_for('index'))
        
        # Create user details
        user_details = UserDetails()
        user_details.redemption_link_id = redemption_link.id
        user_details.full_name = full_name
        user_details.email = email
        user_details.phone = phone
        user_details.address = address
        
        # Mark the redemption link as used immediately
        redemption_link.is_redeemed = True
        redemption_link.redeemed_at = datetime.utcnow()
        
        db.session.add(user_details)
        db.session.commit()
        
        # Clear session
        session.pop('won_product_id', None)
        session.pop('redemption_token', None)
        
        return render_template('details.html', 
                             product=won_product, 
                             success=True,
                             redeemed=True)
    
    return render_template('details.html', product=won_product)

@app.route('/redeem/<token>')
def redeem(token):
    """Handle gift redemption via unique link"""
    # Find redemption link
    redemption_link = RedemptionLink.query.filter_by(token=token).first()
    
    if not redemption_link:
        return render_template('redeem.html', 
                             error='Invalid redemption link.',
                             status='invalid')
    
    if redemption_link.is_redeemed:
        return render_template('redeem.html',
                             product=redemption_link.product,
                             user_details=redemption_link.user_details,
                             status='already_redeemed',
                             redeemed_at=redemption_link.redeemed_at)
    
    # Mark as redeemed
    redemption_link.is_redeemed = True
    redemption_link.redeemed_at = datetime.utcnow()
    db.session.commit()
    
    return render_template('redeem.html',
                         product=redemption_link.product,
                         user_details=redemption_link.user_details,
                         status='success')

@app.route('/admin')
def admin():
    """Admin page to generate and view redemption links"""
    links = RedemptionLink.query.order_by(RedemptionLink.created_at.desc()).all()
    return render_template('admin.html', links=links)

@app.route('/admin/generate', methods=['POST'])
def admin_generate_links():
    """Generate new redemption links"""
    try:
        num_links = int(request.form.get('num_links', 1))
        if num_links < 1 or num_links > 50:
            flash('Number of links must be between 1 and 50.', 'error')
            return redirect(url_for('admin'))
        
        generated_links = []
        for _ in range(num_links):
            redemption_link = RedemptionLink()
            redemption_link.token = RedemptionLink.generate_token()
            redemption_link.is_redeemed = False
            # Don't assign a product yet - it will be randomly selected when scratched
            db.session.add(redemption_link)
            generated_links.append(redemption_link)
        
        db.session.commit()
        flash(f'Successfully generated {num_links} redemption links!', 'success')
        
    except ValueError as e:
        app.logger.error(f'ValueError in admin_generate_links: {e}')
        flash('Invalid number of links specified.', 'error')
    except Exception as e:
        app.logger.error(f'Exception in admin_generate_links: {e}')
        db.session.rollback()
        flash(f'Error generating links: {str(e)}', 'error')
        
    return redirect(url_for('admin'))

@app.route('/scratch/<token>')
def scratch_with_token(token):
    """Scratch card page with pre-generated token"""
    # Find the redemption link
    redemption_link = RedemptionLink.query.filter_by(token=token).first()
    
    if not redemption_link:
        flash('Invalid or expired redemption link.', 'error')
        return redirect(url_for('index'))
    
    if redemption_link.is_redeemed:
        return render_template('redeem.html',
                             product=redemption_link.product,
                             user_details=redemption_link.user_details,
                             status='already_redeemed',
                             redeemed_at=redemption_link.redeemed_at)
    
    # Store the token in session for the scratch process
    session['redemption_token'] = token
    session.pop('won_product_id', None)  # Clear any existing product
    
    return render_template('scratch.html', token=token)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
