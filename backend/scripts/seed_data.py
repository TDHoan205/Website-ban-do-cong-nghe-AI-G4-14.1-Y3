"""
Seed Database Script
Chạy: python -m scripts.seed_data
"""
import sys
sys.path.insert(0, ".")

from app.core.database import SessionLocal, engine, Base
from app.models import (
    User, Product, Category, ProductVariant, ProductImage,
    Supplier, Inventory, Cart, CartItem, Order, OrderItem, Role
)
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random


def seed_roles(db):
    roles = [
        Role(role_id=1, role_name="Admin"),
        Role(role_id=2, role_name="Staff"),
        Role(role_id=3, role_name="Customer"),
    ]
    for role in roles:
        existing = db.query(Role).filter(Role.role_id == role.role_id).first()
        if not existing:
            db.add(role)
    db.commit()
    print("✓ Roles seeded")


def seed_suppliers(db):
    suppliers = [
        Supplier(supplier_id=1, name="Apple Việt Nam", email="contact@apple.vn", phone="1800-1111"),
        Supplier(supplier_id=2, name="Samsung Việt Nam", email="cskh@samsung.vn", phone="1800-2222"),
        Supplier(supplier_id=3, name="Xiaomi Việt Nam", email="support@xiaomi.vn", phone="1800-3333"),
        Supplier(supplier_id=4, name="ASUS Việt Nam", email="info@asus.vn", phone="1800-4444"),
        Supplier(supplier_id=5, name="Dell Việt Nam", email="contact@dell.vn", phone="1800-5555"),
    ]
    for supplier in suppliers:
        existing = db.query(Supplier).filter(Supplier.supplier_id == supplier.supplier_id).first()
        if not existing:
            db.add(supplier)
    db.commit()
    print("✓ Suppliers seeded")


def seed_categories(db):
    categories = [
        Category(category_id=1, name="iPhone", description="Điện thoại iPhone chính hãng Apple"),
        Category(category_id=2, name="Samsung", description="Điện thoại Samsung Galaxy"),
        Category(category_id=3, name="Xiaomi", description="Điện thoại Xiaomi Redmi, POCO"),
        Category(category_id=4, name="MacBook", description="Laptop MacBook Air, MacBook Pro"),
        Category(category_id=5, name="Laptop Gaming", description="Laptop chơi game ASUS ROG, Dell G"),
        Category(category_id=6, name="Laptop Văn phòng", description="Laptop cho công việc hàng ngày"),
        Category(category_id=7, name="Phụ kiện", description="Tai nghe, sạc, ốp lưng, cáp USB"),
    ]
    for cat in categories:
        existing = db.query(Category).filter(Category.category_id == cat.category_id).first()
        if not existing:
            db.add(cat)
    db.commit()
    print("✓ Categories seeded")


def seed_products(db):
    products_data = [
        # iPhone
        {
            "product_id": 1,
            "name": "iPhone 15 Pro Max 256GB",
            "description": "iPhone 15 Pro Max với chip A17 Pro, camera 48MP, màn hình Super Retina XDR 6.7 inch. Thiết kế titanium cao cấp, hỗ trợ USB-C, Action Button. Phù hợp cho người dùng cần hiệu năng cao nhất, chụp ảnh chuyên nghiệp và trải nghiệm giải trí đỉnh cao.",
            "price": 34990000,
            "original_price": 37990000,
            "discount_percent": 8,
            "stock_quantity": 50,
            "rating": 5,
            "is_new": False,
            "is_hot": True,
            "category_id": 1,
            "supplier_id": 1,
            "specifications": '{"chip": "A17 Pro", "ram": "8GB", "display": "6.7 inch Super Retina XDR", "camera": "48MP + 12MP + 12MP", "battery": "4422mAh", "storage": "256GB"}',
            "variants": [
                {"color": "Titan Xám", "storage": "256GB", "price": 34990000},
                {"color": "Titan Xanh", "storage": "256GB", "price": 34990000},
                {"color": "Titan Trắng", "storage": "256GB", "price": 34990000},
                {"color": "Titan Đen", "storage": "512GB", "price": 39990000},
            ]
        },
        {
            "product_id": 2,
            "name": "iPhone 15 128GB",
            "description": "iPhone 15 với chip A16 Bionic, camera 48MP, Dynamic Island. Thiết kế vỏ nhôm và kính mờ cao cấp. Màu sắc tươi sáng, phù hợp với người dùng phổ thông muốn trải nghiệm iOS mới nhất.",
            "price": 22490000,
            "original_price": 24990000,
            "discount_percent": 10,
            "stock_quantity": 100,
            "rating": 5,
            "is_new": False,
            "is_hot": True,
            "category_id": 1,
            "supplier_id": 1,
            "variants": [
                {"color": "Đen", "storage": "128GB", "price": 22490000},
                {"color": "Xanh", "storage": "128GB", "price": 22490000},
                {"color": "Hồng", "storage": "128GB", "price": 22490000},
                {"color": "Vàng", "storage": "256GB", "price": 27490000},
            ]
        },
        # Samsung
        {
            "product_id": 3,
            "name": "Samsung Galaxy S24 Ultra 256GB",
            "description": "Samsung Galaxy S24 Ultra với chip Snapdragon 8 Gen 3, camera 200MP, S Pen tích hợp. Màn hình Dynamic AMOLED 2X 6.8 inch 120Hz. Phù hợp cho doanh nhân và người dùng cần sản phẩm toàn diện nhất.",
            "price": 29990000,
            "original_price": 32990000,
            "discount_percent": 9,
            "stock_quantity": 45,
            "rating": 5,
            "is_new": True,
            "is_hot": True,
            "category_id": 2,
            "supplier_id": 2,
            "variants": [
                {"color": "Titan Đen", "storage": "256GB", "price": 29990000},
                {"color": "Titan Xám", "storage": "256GB", "price": 29990000},
                {"color": "Titan Violet", "storage": "512GB", "price": 33990000},
            ]
        },
        # Xiaomi
        {
            "product_id": 4,
            "name": "Xiaomi 14 Ultra",
            "description": "Xiaomi 14 Ultra với chip Snapdragon 8 Gen 3, camera Leica 50MP. Màn hình AMOLED 6.73 inch 120Hz. Cấu hình flagship với giá cạnh tranh. Phù hợp người dùng muốn trải nghiệm cao cấp với ngân sách hợp lý.",
            "price": 18990000,
            "original_price": 21990000,
            "discount_percent": 14,
            "stock_quantity": 30,
            "rating": 4,
            "is_new": True,
            "is_hot": False,
            "category_id": 3,
            "supplier_id": 3,
            "variants": [
                {"color": "Đen", "storage": "512GB", "price": 18990000},
                {"color": "Trắng", "storage": "512GB", "price": 18990000},
            ]
        },
        # MacBook
        {
            "product_id": 5,
            "name": "MacBook Air M3 13 inch 256GB",
            "description": "MacBook Air M3 với chip Apple M3, hiệu năng vượt trội, pin 18 giờ. Vỏ nhôm tái chế 100%,Silent, không quạt. Phù hợp sinh viên, dân văn phòng, lập trình viên cần di chuyển nhiều.",
            "price": 27990000,
            "original_price": 28990000,
            "discount_percent": 3,
            "stock_quantity": 60,
            "rating": 5,
            "is_new": True,
            "is_hot": False,
            "category_id": 4,
            "supplier_id": 1,
            "variants": [
                {"color": "Bạc", "ram": "8GB", "storage": "256GB", "price": 27990000},
                {"color": "Xám", "ram": "8GB", "storage": "256GB", "price": 27990000},
                {"color": "Vàng", "ram": "16GB", "storage": "512GB", "price": 35990000},
            ]
        },
        {
            "product_id": 6,
            "name": "MacBook Pro 14 inch M3 Pro",
            "description": "MacBook Pro 14 inch với chip M3 Pro, 18GB RAM, 512GB SSD. Màn hình Liquid Retina XDR 14.2 inch. Quạt tản nhiệt hiệu quả cho tác vụ nặng. Phù hợp creative pro: thiết kế đồ họa, video, lập trình chuyên nghiệp.",
            "price": 49990000,
            "original_price": 52990000,
            "discount_percent": 6,
            "stock_quantity": 25,
            "rating": 5,
            "is_new": False,
            "is_hot": True,
            "category_id": 4,
            "supplier_id": 1,
            "variants": [
                {"color": "Bạc", "ram": "18GB", "storage": "512GB", "price": 49990000},
                {"color": "Đen", "ram": "18GB", "storage": "1TB", "price": 59990000},
            ]
        },
        # Laptop Gaming
        {
            "product_id": 7,
            "name": "ASUS ROG Strix G16 G614JZR",
            "description": "Laptop gaming ASUS ROG Strix G16 với CPU Intel i9-14900HX, RTX 4080 12GB, 32GB RAM DDR5, màn hình 16 inch 240Hz. Hiệu năng gaming đỉnh cao, RGB keyboard, hệ thống tản nhiệt thông minh. Phù hợp game thủ hardcore và streamer.",
            "price": 74990000,
            "original_price": 82990000,
            "discount_percent": 10,
            "stock_quantity": 15,
            "rating": 5,
            "is_new": False,
            "is_hot": True,
            "category_id": 5,
            "supplier_id": 4,
            "variants": [
                {"color": "Đen", "ram": "32GB", "storage": "1TB", "price": 74990000},
            ]
        },
        {
            "product_id": 8,
            "name": "Dell G15 5530 Gaming",
            "description": "Laptop Dell G15 với Intel Core i7-13650HX, RTX 4060 8GB, 16GB RAM DDR5, màn hình 15.6 inch 165Hz. Gaming mượt mà, giá hợp lý. Phù hợp sinh viên game thủ hoặc người muốn trải nghiệm gaming tốt với ngân sách vừa phải.",
            "price": 32990000,
            "original_price": 35990000,
            "discount_percent": 8,
            "stock_quantity": 40,
            "rating": 4,
            "is_new": False,
            "is_hot": True,
            "category_id": 5,
            "supplier_id": 5,
            "variants": [
                {"color": "Đen", "ram": "16GB", "storage": "512GB", "price": 32990000},
                {"color": "Xanh", "ram": "16GB", "storage": "1TB", "price": 37990000},
            ]
        },
        # Laptop Văn phòng
        {
            "product_id": 9,
            "name": "ASUS ZenBook 14 OLED",
            "description": "Laptop ASUS ZenBook 14 OLED với Intel Core Ultra 7, 16GB RAM, 512GB SSD, màn hình OLED 14 inch 2.8K 90Hz. Siêu mỏng nhẹ 1.2kg, pin 15 giờ. Phù hợp dân văn phòng, doanh nhân cần di chuyển nhiều.",
            "price": 26990000,
            "original_price": 29990000,
            "discount_percent": 10,
            "stock_quantity": 35,
            "rating": 5,
            "is_new": True,
            "is_hot": False,
            "category_id": 6,
            "supplier_id": 4,
            "variants": [
                {"color": "Xanh", "ram": "16GB", "storage": "512GB", "price": 26990000},
                {"color": "Xám", "ram": "16GB", "storage": "1TB", "price": 30990000},
            ]
        },
        {
            "product_id": 10,
            "name": "MacBook Air M1 2020",
            "description": "MacBook Air M1 với chip Apple M1, 8GB RAM, 256GB SSD. Siêu mỏng, không quạt, pin 18 giờ. Hiệu năng tốt cho công việc văn phòng, lập trình web, học tập. Lựa chọn budget tốt nhất cho macOS.",
            "price": 19990000,
            "original_price": 22990000,
            "discount_percent": 13,
            "stock_quantity": 80,
            "rating": 4,
            "is_new": False,
            "is_hot": True,
            "category_id": 6,
            "supplier_id": 1,
            "variants": [
                {"color": "Vàng", "ram": "8GB", "storage": "256GB", "price": 19990000},
                {"color": "Bạc", "ram": "8GB", "storage": "256GB", "price": 19990000},
            ]
        },
        # Phụ kiện
        {
            "product_id": 11,
            "name": "AirPods Pro 2 USB-C",
            "description": "Tai nghe AirPods Pro 2 với USB-C, chống ồn chủ động ANC, Transparency mode, Spatial Audio. Pin 6 giờ (tai nghe) + 30 giờ (hộp sạc). Phù hợp người dùng iPhone cần tai nghe chống ồn cao cấp.",
            "price": 5990000,
            "original_price": 6490000,
            "discount_percent": 8,
            "stock_quantity": 120,
            "rating": 5,
            "is_new": False,
            "is_hot": True,
            "category_id": 7,
            "supplier_id": 1,
            "variants": [
                {"color": "Trắng", "price": 5990000},
            ]
        },
        {
            "product_id": 12,
            "name": "Samsung Galaxy Buds2 Pro",
            "description": "Tai nghe Samsung Galaxy Buds2 Pro với ANC thông minh, âm thanh 360 Audio, chống nước IPX7. Kết nối đa điểm, chuyển đổi linh hoạt giữa thiết bị. Phù hợp người dùng Samsung Galaxy và Android.",
            "price": 4990000,
            "original_price": 5490000,
            "discount_percent": 9,
            "stock_quantity": 90,
            "rating": 4,
            "is_new": False,
            "is_hot": False,
            "category_id": 7,
            "supplier_id": 2,
            "variants": [
                {"color": "Đen", "price": 4990000},
                {"color": "Trắng", "price": 4990000},
                {"color": "Tím", "price": 4990000},
            ]
        },
    ]

    for p_data in products_data:
        variants_data = p_data.pop("variants", [])

        existing = db.query(Product).filter(Product.product_id == p_data["product_id"]).first()
        if not existing:
            product = Product(**p_data)
            db.add(product)
            db.commit()

            for i, v in enumerate(variants_data):
                variant = ProductVariant(
                    product_id=product.product_id,
                    color=v.get("color"),
                    storage=v.get("storage"),
                    ram=v.get("ram"),
                    price=v.get("price", product.price),
                    display_order=i,
                )
                db.add(variant)

            inventory = Inventory(
                product_id=product.product_id,
                quantity=product.stock_quantity,
                min_stock_level=5,
            )
            db.add(inventory)
            db.commit()

    print("✓ Products seeded")


def seed_users(db):
    users = [
        {
            "user_id": 1,
            "username": "admin",
            "email": "admin@techstore.vn",
            "full_name": "Quản trị viên",
            "phone": "0912345678",
            "address": "123 Nguyễn Trãi, Q1, TP.HCM",
            "role_id": 1,
            "password_hash": get_password_hash("admin123"),
        },
        {
            "user_id": 2,
            "username": "staff01",
            "email": "staff01@techstore.vn",
            "full_name": "Nhân viên 01",
            "phone": "0912345679",
            "role_id": 2,
            "password_hash": get_password_hash("staff123"),
        },
        {
            "user_id": 3,
            "username": "customer01",
            "email": "nguyenvana@gmail.com",
            "full_name": "Nguyễn Văn A",
            "phone": "0912345680",
            "address": "456 Lê Lợi, Q3, TP.HCM",
            "role_id": 3,
            "password_hash": get_password_hash("customer123"),
        },
    ]

    for u_data in users:
        existing = db.query(User).filter(User.user_id == u_data["user_id"]).first()
        if not existing:
            user = User(**u_data)
            db.add(user)
    db.commit()
    print("✓ Users seeded")


def seed_sample_orders(db):
    user = db.query(User).filter(User.username == "customer01").first()
    if not user:
        print("Skip orders - no user")
        return

    existing_orders = db.query(Order).filter(Order.user_id == user.user_id).count()
    if existing_orders > 0:
        print("Skip orders - already exist")
        return

    order = Order(
        user_id=user.user_id,
        total_amount=59980000,
        status="Delivered",
        customer_name=user.full_name,
        customer_phone=user.phone,
        customer_address=user.address,
        order_date=datetime.now() - timedelta(days=5),
    )
    db.add(order)
    db.commit()

    order_items = [
        OrderItem(order_id=order.order_id, product_id=1, quantity=1, unit_price=34990000),
        OrderItem(order_id=order.order_id, product_id=11, quantity=2, unit_price=5990000),
    ]
    for item in order_items:
        db.add(item)
    db.commit()
    print("✓ Sample orders seeded")


def run_seed():
    print("🚀 Starting database seed...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        seed_roles(db)
        seed_suppliers(db)
        seed_categories(db)
        seed_products(db)
        seed_users(db)
        seed_sample_orders(db)

        print("\n✅ Database seeded successfully!")
        print("\n📋 Test accounts:")
        print("  Admin:    admin / admin123")
        print("  Staff:    staff01 / staff123")
        print("  Customer: customer01 / customer123")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
