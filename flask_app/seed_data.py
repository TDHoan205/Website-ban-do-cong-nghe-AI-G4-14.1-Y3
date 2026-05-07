"""
Seed data script – populates SQL Server with initial data.
Run AFTER SQL/schema.sql has been executed.
Usage: python flask_app/seed_data.py
"""
import os
import sys

# Add project root (parent of flask_app/) so flask_app.* imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from flask_app.database import SessionLocal
from flask_app.models import Role, Category, Supplier, Product, ProductVariant, ProductImage, Account

# bcrypt is only imported here (lazy) to avoid import errors on systems without it
def _hash(password: str) -> str:
    import bcrypt
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _ensure_role(db: Session, name: str, description: str = "") -> Role:
    r = db.query(Role).filter(Role.role_name == name).first()
    if not r:
        r = Role(role_name=name, description=description)
        db.add(r)
        db.commit()
        db.refresh(r)
    return r


def seed_roles(db: Session):
    _ensure_role(db, "Admin", "Quản trị viên")
    _ensure_role(db, "Employee", "Nhân viên")
    _ensure_role(db, "Customer", "Khách hàng")
    print("  [OK] Roles seeded")


def seed_categories(db: Session):
    cats = [
        ("Điện thoại", "Điện thoại thông minh các hãng: iPhone, Samsung, Xiaomi...", "phone"),
        ("Laptop", "Máy tính xách tay: MacBook, Dell, HP, ASUS...", "laptop"),
        ("Tablet", "Máy tính bảng: iPad, Galaxy Tab...", "tablet"),
        ("Tai nghe", "Tai nghe không dây và có dây chất lượng cao", "headphones"),
        ("Đồng hồ thông minh", "Smartwatch Apple, Samsung, Garmin...", "watch"),
        ("Phụ kiện", "Sạc, cáp, ốp lưng, chuột, bàn phím...", "accessory"),
    ]
    for name, desc, _ in cats:
        if not db.query(Category).filter(Category.name == name).first():
            db.add(Category(name=name, description=desc))
    db.commit()
    print("  [OK] Categories seeded")


def seed_suppliers(db: Session):
    suppliers = [
        ("Apple Việt Nam", "Nguyễn Văn A", "0123456789", "apple@vendor.com", "TP.HCM"),
        ("Samsung Việt Nam", "Trần Thị B", "0987654321", "samsung@vendor.com", "Hà Nội"),
        ("Sony Việt Nam", "Lê Văn C", "0369852147", "sony@vendor.com", "Đà Nẵng"),
    ]
    for name, contact, phone, email, addr in suppliers:
        if not db.query(Supplier).filter(Supplier.name == name).first():
            db.add(Supplier(name=name, contact_person=contact, phone=phone, email=email, address=addr))
    db.commit()
    print("  [OK] Suppliers seeded")


def seed_products(db: Session):
    phone = db.query(Category).filter(Category.name == "Điện thoại").first()
    laptop = db.query(Category).filter(Category.name == "Laptop").first()
    headphone = db.query(Category).filter(Category.name == "Tai nghe").first()
    watch = db.query(Category).filter(Category.name == "Đồng hồ thông minh").first()
    accessory = db.query(Category).filter(Category.name == "Phụ kiện").first()
    tablet = db.query(Category).filter(Category.name == "Tablet").first()

    products = [
        # Điện thoại
        dict(name="iPhone 15 Pro Max", description="Flagship Apple với chip A17 Pro, camera 48MP, màn hình OLED 6.7 inch. Thiết kế titanium cao cấp, pin trâu, hệ sinh thái Apple hoàn hảo.", price=34990000, original_price=37990000, stock_quantity=50, rating=4.9, is_new=True, is_hot=True, discount_percent=8, specifications="A17 Pro, 8GB RAM, 256GB, 5G", category=phone),
        dict(name="Samsung Galaxy S24 Ultra", description="Flagship Android với camera 200MP, S Pen tích hợp, AI features thông minh. Màn hình Dynamic AMOLED 2X 6.8 inch.", price=32990000, original_price=34990000, stock_quantity=40, rating=4.8, is_new=True, is_hot=True, discount_percent=6, specifications="Snapdragon 8 Gen 3, 12GB RAM, 256GB, 5G", category=phone),
        dict(name="iPhone 14", description="iPhone thế hệ trước với chip A15 Bionic, camera 12MP, màn hình Super Retina XDR 6.1 inch. Hiệu năng mạnh mẽ, giá hợp lý.", price=22990000, stock_quantity=80, rating=4.7, is_new=False, is_hot=True, discount_percent=0, specifications="A15 Bionic, 6GB RAM, 128GB, 5G", category=phone),
        dict(name="Samsung Galaxy A55 5G", description="Điện thoại tầm trung với màn hình Super AMOLED 6.6 inch, camera 50MP, pin 5000mAh. Thiết kế thời trang, giá cả hợp lý.", price=9990000, original_price=11990000, stock_quantity=120, rating=4.5, is_new=True, is_hot=False, discount_percent=17, specifications="Exynos 1480, 8GB RAM, 128GB, 5G", category=phone),
        dict(name="Xiaomi 13T Pro", description="Flagship killer với camera Leica 200MP, chip Dimensity 9200+, sạc nhanh 120W. Màn hình AMOLED 144Hz.", price=14990000, original_price=16990000, stock_quantity=60, rating=4.6, is_new=True, is_hot=True, discount_percent=12, specifications="Dimensity 9200+, 12GB RAM, 256GB, 5G", category=phone),
        # Laptop
        dict(name="MacBook Pro 14 M3", description="Laptop chuyên nghiệp với chip M3, 18GB RAM, 512GB SSD. Màn hình Liquid Retina XDR 14.2 inch, pin 17h.", price=45990000, original_price=49990000, stock_quantity=20, rating=4.9, is_new=True, is_hot=True, discount_percent=8, specifications="Apple M3, 18GB RAM, 512GB SSD, macOS", category=laptop),
        dict(name="Dell XPS 15", description="Laptop cao cấp Windows với Intel Core i9, 32GB RAM, 1TB SSD. Màn hình OLED 3.5K 15.6 inch tuyệt đẹp.", price=58990000, stock_quantity=15, rating=4.6, is_new=False, is_hot=True, discount_percent=0, specifications="Intel Core i9-13900H, 32GB RAM, 1TB SSD, RTX 4060", category=laptop),
        dict(name="MacBook Air M3 15", description="Laptop mỏng nhẹ với chip M3, 16GB RAM, 256GB SSD. Màn hình Liquid Retina 15.3 inch, pin 18h.", price=35990000, stock_quantity=35, rating=4.8, is_new=True, is_hot=True, discount_percent=0, specifications="Apple M3, 16GB RAM, 256GB SSD, macOS", category=laptop),
        dict(name="HP Pavilion Plus 14", description="Laptop văn phòng mỏng nhẹ với Intel Core i7 thế hệ 13, 16GB RAM, 512GB SSD. Màn hình OLED 2.8K 14 inch.", price=24990000, stock_quantity=45, rating=4.4, is_new=True, is_hot=False, discount_percent=0, specifications="Intel Core i7-13700H, 16GB RAM, 512GB SSD, OLED 2.8K", category=laptop),
        dict(name="Lenovo ThinkPad X1 Carbon", description="Laptop doanh nhân siêu nhẹ 1.12kg, Intel Core i7, 16GB RAM. Được tin dùng bởi các doanh nghiệp hàng đầu.", price=47990000, stock_quantity=25, rating=4.7, is_new=False, is_hot=True, discount_percent=0, specifications="Intel Core i7-1365U, 16GB RAM, 512GB SSD, LTE", category=laptop),
        # Tai nghe
        dict(name="AirPods Pro 2", description="Tai nghe không dây chống ồn chủ động ANC, Spatial Audio, sạc USB-C. Chip H2, pin 6h, chống nước IPX4.", price=6990000, stock_quantity=100, rating=4.8, is_new=True, is_hot=True, discount_percent=0, specifications="H2 chip, ANC, Spatial Audio, USB-C, IPX4", category=headphone),
        dict(name="Sony WH-1000XM5", description="Tai nghe over-ear chống ồn tốt nhất thế giới. Thiết kế mới, driver 30mm, LDAC, pin 30h.", price=8990000, original_price=9990000, stock_quantity=60, rating=4.9, is_new=True, is_hot=True, discount_percent=10, specifications="30mm driver, ANC, LDAC, 30h pin, USB-C", category=headphone),
        dict(name="Samsung Galaxy Buds2 Pro", description="Tai nghe true wireless chống ồn với 360 Audio, IPX7, codec SSC Hi-Fi. Thiết kế nhỏ gọn, âm thanh tuyệt vời.", price=4990000, original_price=5990000, stock_quantity=80, rating=4.6, is_new=False, is_hot=True, discount_percent=17, specifications="ANC, 360 Audio, IPX7, 5h pin, USB-C", category=headphone),
        dict(name="JBL Tune 770NC", description="Tai nghe over-ear chống ồn giá rẻ, pin 70h, Bluetooth 5.3. Âm bass mạnh mẽ, thoải mái đeo cả ngày.", price=2990000, stock_quantity=90, rating=4.4, is_new=False, is_hot=False, discount_percent=0, specifications="ANC, 70h pin, Bluetooth 5.3, JBL Pure Bass Sound", category=headphone),
        # Đồng hồ
        dict(name="Apple Watch Ultra 2", description="Đồng hồ thông minh cho thể thao mạnh mẽ, GPS chính xác, pin 36h, titanium grade 5, chống nước 100m.", price=18990000, stock_quantity=30, rating=4.8, is_new=True, is_hot=True, discount_percent=0, specifications="S9 SiP, 36h pin, GPS + LTE, 100m WR, titanium", category=watch),
        dict(name="Samsung Galaxy Watch 6 Classic", description="Đồng hồ Android tốt nhất với màn hình AMOLED xoay bezel, ECG, SpO2, theo dõi sức khỏe toàn diện.", price=8990000, original_price=9990000, stock_quantity=50, rating=4.7, is_new=False, is_hot=True, discount_percent=10, specifications="Exynos W930, 1.5GB RAM, 16GB, AMOLED, 40mm", category=watch),
        dict(name="Apple Watch Series 9", description="Đồng hồ phổ biến nhất với chip S9, màn hình Always-On, ECG, SpO2. Hệ sinh thái Apple hoàn hảo.", price=11990000, stock_quantity=70, rating=4.9, is_new=True, is_hot=True, discount_percent=0, specifications="S9 SiP, 45mm, Always-On, GPS, IP6X", category=watch),
        # Tablet
        dict(name="iPad Pro M4 12.9", description="Tablet mạnh nhất thế giới với chip M4, màn hình Liquid Retina XDR 12.9 inch, hỗ trợ Apple Pencil Pro.", price=31990000, stock_quantity=25, rating=4.9, is_new=True, is_hot=True, discount_percent=0, specifications="Apple M4, 8GB RAM, 256GB, Liquid Retina XDR", category=tablet),
        dict(name="Samsung Galaxy Tab S9 Ultra", description="Tablet Android cao cấp với màn hình Dynamic AMOLED 2X 14.6 inch, S Pen, chip Snapdragon 8 Gen 2.", price=27990000, original_price=30990000, stock_quantity=30, rating=4.7, is_new=False, is_hot=True, discount_percent=10, specifications="SD 8 Gen 2, 12GB RAM, 256GB, S Pen, AMOLED 14.6", category=tablet),
        # Phụ kiện
        dict(name="Anker PowerCore 20000mAh", description="Sạc dự phòng 20000mAh, sạc nhanh PowerIQ 3.0, 2 cổng USB-A + 1 USB-C. Sạc được laptop.", price=1290000, stock_quantity=200, rating=4.7, is_new=False, is_hot=True, discount_percent=0, specifications="20000mAh, 65W USB-C PD, PowerIQ 3.0", category=accessory),
        dict(name="Anker 735 65W GaN", description="Sạc GaN 3 cổng 65W siêu nhỏ gọn. Sạc laptop, điện thoại, tablet cùng lúc. Công nghệ GaN II.", price=1590000, stock_quantity=150, rating=4.8, is_new=True, is_hot=True, discount_percent=0, specifications="65W PD, GaN II, 3 cổng (2 USB-C + 1 USB-A)", category=accessory),
        dict(name="Samsung T7 1TB", description="Ổ SSD di động USB-C 3.2 Gen 2, tốc độ 1050MB/s, nhỏ gọn, chống sốc. Lưu trữ nhanh và an toàn.", price=3490000, stock_quantity=100, rating=4.8, is_new=False, is_hot=True, discount_percent=0, specifications="1TB, USB-C 3.2 Gen2, 1050MB/s, 58g", category=accessory),
        dict(name="Logitech MX Master 3S", description="Chuột không dây cao cấp với cuộn MagSpeed, theo dõi 8000 DPI, kết nối 3 thiết bị. Ergonomic design.", price=3290000, stock_quantity=80, rating=4.9, is_new=True, is_hot=True, discount_percent=0, specifications="8000 DPI, MagSpeed, Bluetooth + USB receiver, 70 days", category=accessory),
        dict(name="Logitech G Pro X Superlight 2", description="Chuột gaming siêu nhẹ 60g, HERO 25K sensor, Lightspeed wireless, pin 70h. Chuột esports chuyên nghiệp.", price=4990000, stock_quantity=40, rating=4.9, is_new=True, is_hot=True, discount_percent=0, specifications="60g, HERO 25K, Lightspeed, 70h pin, PMW", category=accessory),
    ]

    for pdata in products:
        if db.query(Product).filter(Product.name == pdata["name"]).first():
            continue
        cat = pdata.pop("category")
        product = Product(**pdata, category_id=cat.category_id if cat else None)
        db.add(product)
    db.commit()
    print("  [OK] Products seeded")


def seed_variants(db: Session):
    """Add product variants for products that have them."""
    # Get products
    iphone = db.query(Product).filter(Product.name == "iPhone 15 Pro Max").first()
    galaxy = db.query(Product).filter(Product.name == "Samsung Galaxy S24 Ultra").first()
    macbook = db.query(Product).filter(Product.name == "MacBook Pro 14 M3").first()
    xiaomi = db.query(Product).filter(Product.name == "Xiaomi 13T Pro").first()

    variants_data = [
        (iphone, [("Titan tự nhiên", "256GB"), ("Titan xanh dương", "256GB"), ("Titan trắng", "512GB"), ("Titan đen", "1TB")]),
        (galaxy, [("Đen Titanium", "256GB"), ("Xám Titanium", "512GB"), ("Tím Titanium", "512GB")]),
        (macbook, [("Space Black", "512GB"), ("Bạc", "512GB"), ("Space Black", "1TB")]),
        (xiaomi, [("Đen", "256GB"), ("Xanh lá", "256GB"), ("Đen", "512GB")]),
    ]

    for product, variants in variants_data:
        if not product:
            continue
        for color, storage in variants:
            if not db.query(ProductVariant).filter(
                ProductVariant.product_id == product.product_id,
                ProductVariant.color == color,
                ProductVariant.storage == storage,
            ).first():
                db.add(ProductVariant(
                    product_id=product.product_id,
                    color=color,
                    storage=storage,
                    variant_name=f"{color} / {storage}",
                    price=product.price,
                    stock_quantity=product.stock_quantity,
                    is_active=True,
                ))
    db.commit()
    print("  [OK] Product variants seeded")


def seed_accounts(db: Session):
    admin_role = db.query(Role).filter(Role.role_name == "Admin").first()
    customer_role = db.query(Role).filter(Role.role_name == "Customer").first()

    # Admin account
    if not db.query(Account).filter(Account.username == "admin").first():
        db.add(Account(
            username="admin",
            email="admin@techstore.com",
            password_hash=_hash("admin123"),
            full_name="Quản trị viên",
            phone="0123456789",
            role_id=admin_role.role_id,
            is_active=True,
        ))

    # Demo customer accounts
    for i in range(1, 4):
        username = f"customer{i}"
        if not db.query(Account).filter(Account.username == username).first():
            db.add(Account(
                username=username,
                email=f"customer{i}@techstore.com",
                password_hash=_hash("customer123"),
                full_name=f"Khách hàng Demo {i}",
                phone=f"098765432{i}",
                role_id=customer_role.role_id,
                is_active=True,
            ))

    db.commit()
    print("  [OK] Accounts seeded")


def main():
    print("\n=== Seeding database... ===\n")
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_categories(db)
        seed_suppliers(db)
        seed_products(db)
        seed_variants(db)
        seed_accounts(db)
        print("\n=== Seed complete! ===")
        print("  Admin login: admin / admin123")
        print("  Customer login: customer1 / customer123\n")
    finally:
        db.close()


if __name__ == "__main__":
    main()
