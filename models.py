from app import db
from datetime import datetime
import secrets
import string

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'

class RedemptionLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    is_redeemed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    redeemed_at = db.Column(db.DateTime)
    
    # Relationship to Product
    product = db.relationship('Product', backref=db.backref('redemption_links', lazy=True))
    
    # Relationship to UserDetails
    user_details = db.relationship('UserDetails', backref='redemption_link', uselist=False)

    def __repr__(self):
        return f'<RedemptionLink {self.token}>'
    
    @staticmethod
    def generate_token():
        """Generate a secure random token"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(32))

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    redemption_link_id = db.Column(db.Integer, db.ForeignKey('redemption_link.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserDetails {self.full_name}>'
