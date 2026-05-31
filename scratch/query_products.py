import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Data.database import SessionLocal
from Models.Product import Product

db = SessionLocal()
try:
    banner_products = []
    prod_1 = db.query(Product).filter(Product.product_id == 1).first()
    if prod_1:
        banner_products.append(prod_1)
    
    other_products = db.query(Product).filter(
        Product.product_id != 1,
        Product.is_available == True,
        Product.image_url != None
    ).order_by(Product.is_hot.desc(), Product.created_at.desc()).limit(4).all()
    
    banner_products.extend(other_products)

    print(f"Total banner products: {len(banner_products)}")
    for p in banner_products:
        print(f"ID: {p.product_id} | Name: {p.name} | Price: {p.price} | Image: {p.first_image_url} | IsHot: {p.is_hot}")
finally:
    db.close()
