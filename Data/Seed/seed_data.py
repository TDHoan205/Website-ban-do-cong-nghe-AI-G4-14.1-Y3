"""
Seed Data - Tạo dữ liệu mẫu
Tương đương Data/Seed/SeedData.cs trong ASP.NET Core
"""
import sys
import os

# Thêm thư mục gốc vào PYTHONPATH để có thể import Models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy.orm import Session
from Models.Category import Category
from Models.Supplier import Supplier
from Models.Product import Product
from Models.Account import Account, Role
from Services.AuthService import AuthService
from datetime import datetime


def seed_categories(db: Session):
    """Tạo dữ liệu danh mục mẫu"""
    categories = [
        {"name": "Điện thoại", "description": "Điện thoại thông minh các hãng", "image_url": "https://via.placeholder.com/200x200?text=Phone"},
        {"name": "Laptop", "description": "Máy tính xách tay", "image_url": "https://via.placeholder.com/200x200?text=Laptop"},
        {"name": "Tablet", "description": "Máy tính bảng", "image_url": "https://via.placeholder.com/200x200?text=Tablet"},
        {"name": "Tai nghe", "description": "Tai nghe không dây và có dây", "image_url": "https://via.placeholder.com/200x200?text=Headphone"},
        {"name": "Đồng hồ thông minh", "description": "Smartwatch các hãng", "image_url": "https://via.placeholder.com/200x200?text=Watch"},
        {"name": "Phụ kiện", "description": "Sạc, cáp, ốp lưng...", "image_url": "https://via.placeholder.com/200x200?text=Accessory"},
    ]

    for cat_data in categories:
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)

    db.commit()
    print("✓ Đã tạo dữ liệu danh mục")


def seed_suppliers(db: Session):
    """Tạo dữ liệu nhà cung cấp mẫu"""
    suppliers = [
        {"name": "Apple Việt Nam", "contact_person": "Nguyễn Văn A", "phone": "0123456789", "email": "apple@vendor.com"},
        {"name": "Samsung Việt Nam", "contact_person": "Trần Thị B", "phone": "0987654321", "email": "samsung@vendor.com"},
        {"name": "Sony Việt Nam", "contact_person": "Lê Văn C", "phone": "0369852147", "email": "sony@vendor.com"},
    ]

    for sup_data in suppliers:
        existing = db.query(Supplier).filter(Supplier.name == sup_data["name"]).first()
        if not existing:
            supplier = Supplier(**sup_data)
            db.add(supplier)

    db.commit()
    print("✓ Đã tạo dữ liệu nhà cung cấp")


def seed_products(db: Session):
    """Tạo dữ liệu sản phẩm mẫu"""
    # Lấy category IDs
    phone_cat = db.query(Category).filter(Category.name == "Điện thoại").first()
    laptop_cat = db.query(Category).filter(Category.name == "Laptop").first()
    headphone_cat = db.query(Category).filter(Category.name == "Tai nghe").first()
    watch_cat = db.query(Category).filter(Category.name == "Đồng hồ thông minh").first()

    products = [
        # Điện thoại
        {
            "name": "iPhone 15 Pro Max",
            "description": "Điện thoại flagship của Apple với chip A17 Pro, camera 48MP, màn hình OLED 6.7 inch",
            "image_url": "https://via.placeholder.com/400x400?text=iPhone+15+Pro+Max",
            "price": 34990000,
            "original_price": 37990000,
            "stock_quantity": 50,
            "rating": 4.9,
            "is_new": True,
            "is_hot": True,
            "discount_percent": 8,
            "specifications": "A17 Pro, 8GB RAM, 256GB, 5G",
            "category_id": phone_cat.category_id if phone_cat else None,
        },
        {
            "name": "Samsung Galaxy S24 Ultra",
            "description": "Flagship Android với camera 200MP, S Pen tích hợp, AI features",
            "image_url": "https://via.placeholder.com/400x400?text=Galaxy+S24+Ultra",
            "price": 32990000,
            "original_price": 34990000,
            "stock_quantity": 40,
            "rating": 4.8,
            "is_new": True,
            "is_hot": True,
            "discount_percent": 6,
            "category_id": phone_cat.category_id if phone_cat else None,
        },
        {
            "name": "iPhone 14",
            "description": "iPhone thế hệ trước với chip A15 Bionic, camera 12MP",
            "image_url": "https://via.placeholder.com/400x400?text=iPhone+14",
            "price": 22990000,
            "stock_quantity": 80,
            "rating": 4.7,
            "is_new": False,
            "is_hot": True,
            "category_id": phone_cat.category_id if phone_cat else None,
        },
        # Laptop
        {
            "name": "MacBook Pro M3 14 inch",
            "description": "Laptop chuyên nghiệp với chip M3, 18GB RAM, 512GB SSD",
            "image_url": "https://via.placeholder.com/400x400?text=MacBook+Pro+M3",
            "price": 45990000,
            "original_price": 49990000,
            "stock_quantity": 20,
            "rating": 4.9,
            "is_new": True,
            "is_hot": True,
            "discount_percent": 8,
            "category_id": laptop_cat.category_id if laptop_cat else None,
        },
        {
            "name": "Dell XPS 15",
            "description": "Laptop cao cấp Windows với Intel Core i9, 32GB RAM",
            "image_url": "https://via.placeholder.com/400x400?text=Dell+XPS+15",
            "price": 38990000,
            "stock_quantity": 15,
            "rating": 4.6,
            "is_new": False,
            "is_hot": True,
            "category_id": laptop_cat.category_id if laptop_cat else None,
        },
        # Tai nghe
        {
            "name": "AirPods Pro 2",
            "description": "Tai nghe không dây chống ồn chủ động, Spatial Audio",
            "image_url": "https://via.placeholder.com/400x400?text=AirPods+Pro+2",
            "price": 6990000,
            "stock_quantity": 100,
            "rating": 4.8,
            "is_new": True,
            "is_hot": True,
            "category_id": headphone_cat.category_id if headphone_cat else None,
        },
        {
            "name": "Sony WH-1000XM5",
            "description": "Tai nghe over-ear chống ồn tốt nhất",
            "image_url": "https://via.placeholder.com/400x400?text=Sony+XM5",
            "price": 8990000,
            "original_price": 9990000,
            "stock_quantity": 60,
            "rating": 4.9,
            "is_new": True,
            "is_hot": True,
            "discount_percent": 10,
            "category_id": headphone_cat.category_id if headphone_cat else None,
        },
        # Đồng hồ
        {
            "name": "Apple Watch Ultra 2",
            "description": "Đồng hồ thông minh cho thể thao mạnh mẽ",
            "image_url": "https://via.placeholder.com/400x400?text=Watch+Ultra+2",
            "price": 18990000,
            "stock_quantity": 30,
            "rating": 4.8,
            "is_new": True,
            "is_hot": True,
            "category_id": watch_cat.category_id if watch_cat else None,
        },
    ]

    for prod_data in products:
        existing = db.query(Product).filter(Product.name == prod_data["name"]).first()
        if not existing:
            product = Product(**prod_data)
            db.add(product)

    db.commit()
    print("✓ Đã tạo dữ liệu sản phẩm")


def seed_admin_user(db: Session):
    """Tạo tài khoản admin mặc định"""
    auth_service = AuthService(db)

    admin_role = db.query(Role).filter(Role.role_name == "Admin").first()
    if not admin_role:
        admin_role = Role(role_name="Admin", description="Administrator")
        db.add(admin_role)

    customer_role = db.query(Role).filter(Role.role_name == "Customer").first()
    if not customer_role:
        customer_role = Role(role_name="Customer", description="Default customer role")
        db.add(customer_role)

    db.commit()

    admin = auth_service.get_account_by_username("admin")
    if not admin:
        account = Account(
            username="admin",
            email="admin@techstore.com",
            password_hash=auth_service.hash_password("admin123"),
            full_name="Administrator",
            phone="0123456789",
            role_id=admin_role.role_id,
            is_active=True
        )
        db.add(account)
        db.commit()
        print("✓ Đã tạo tài khoản admin (admin / admin123)")
    else:
        print("✓ Tài khoản admin đã tồn tại")


def seed_all(db: Session):
    """Chạy tất cả seed data"""
    print("\n=== Bắt đầu seed dữ liệu ===\n")

    seed_categories(db)
    seed_suppliers(db)
    seed_products(db)
    seed_admin_user(db)

    print("\n=== Hoàn thành seed dữ liệu ===\n")


if __name__ == "__main__":
    from Data.database import SessionLocal

    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()
