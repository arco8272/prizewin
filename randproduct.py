from app import app, db
from models import Product

def init_products():
    with app.app_context():
        if Product.query.count() == 0:
            default_products = [
                {
                    'name': 'Chopper',
                    'description': 'Vegetable chopper',
                    'image_url': 'https://rukminim2.flixcart.com/image/300/300/jvsf3ww0/chopper/f/w/z/green-combo-of-3-piece-vegetable-peeler-and-cutter-home-use-2-in-original-imafgmjbnthpyw4y.jpeg?q=90'
                },
                {
                    'name': 'Special Doremon box',
                    'description': 'pencil box ',
                    'image_url': 'https://www.bing.com/th/id/OIP.hms02f_8HIPt0rhs0IepAwHaGj?w=233&h=211&c=8&rs=1&qlt=90&o=6&pid=3.1&rm=2'
                },
                {
                    'name': 'NotePad',
                    'description': 'notdpad',
                    'image_url': 'https://www.bing.com/th?id=OPAC.kQLC33TF69MRwg474C474&o=5&pid=21.1&w=128&h=188&rs=1&qlt=100&dpr=1&o=2&bw=6&bc=FFFFFF'
                },
                {
                    'name': 'bottle',
                    'description': 'water bottle',
                    'image_url': 'https://www.bing.com/th?id=OPAC.4Aeutw9XfT91mw474C474&o=5&pid=21.1&w=128&h=188&rs=1&qlt=100&dpr=1&o=2&bw=6&bc=FFFFFF'
                },
                {
                    'name': '',
                    'description': 'perfume',
                    'image_url': 'https://m.media-amazon.com/images/I/81ZX7Qw5aNL._SL1500_.jpg'
                }
            ]
            
            for product_data in default_products:
                # Clean the product name for database storage
                clean_name = product_data['name'].replace('£', 'GBP').replace('$', 'USD')
                product_data['name'] = clean_name
                product = Product(**product_data)
                db.session.add(product)
            
            db.session.commit()