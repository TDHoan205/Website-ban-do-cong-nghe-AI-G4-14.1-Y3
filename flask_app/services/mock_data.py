"""
Mock data service – all fake data for the Flask demo.
No database required; everything is in-memory.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import random

from ..models.schemas import (
    Product, ProductVariant, ProductCategory, ProductSupplier,
    CartItem, Order, Account, Category, Supplier,
    StatisticsViewModel, RevenueDay, TopProduct, RecentOrder,
    PaginatedProducts,
)


# ══════════════════════════════════════════════════════════════
# CATEGORIES
# ══════════════════════════════════════════════════════════════
CATEGORIES: List[Category] = [
    Category(category_id=1, name="Điện thoại", description="Smartphone các hãng"),
    Category(category_id=2, name="Laptop", description="Máy tính xách tay"),
    Category(category_id=3, name="Tablet", description="Máy tính bảng"),
    Category(category_id=4, name="Âm thanh", description="Tai nghe, loa"),
    Category(category_id=5, name="Đồng hồ", description="Smartwatch, đồng hồ thông minh"),
    Category(category_id=6, name="Phụ kiện", description="Sạc, cáp, ốp lưng"),
    Category(category_id=7, name="Camera", description="Webcam, action cam"),
    Category(category_id=8, name="Bàn phím & Chuột", description="Bàn phím, chuột máy tính"),
]

CAT_MAP: Dict[int, Category] = {c.category_id: c for c in CATEGORIES}
CAT_NAME_MAP: Dict[str, Category] = {c.name: c for c in CATEGORIES}


# ══════════════════════════════════════════════════════════════
# SUPPLIERS
# ══════════════════════════════════════════════════════════════
SUPPLIERS: List[Supplier] = [
    Supplier(supplier_id=1, name="Apple Vietnam", contact_name="Nguyễn Văn A",
             phone="0901234567", email="apple@supplier.vn",
             address="Quận 1, TP.HCM"),
    Supplier(supplier_id=2, name="Samsung Electronics VN", contact_name="Trần Thị B",
             phone="0902345678", email="samsung@supplier.vn",
             address="Quận 7, TP.HCM"),
    Supplier(supplier_id=3, name="Xiaomi Việt Nam", contact_name="Lê Văn C",
             phone="0903456789", email="xiaomi@supplier.vn",
             address="Quận 3, TP.HCM"),
    Supplier(supplier_id=4, name="Anker Vietnam", contact_name="Phạm Thị D",
             phone="0904567890", email="anker@supplier.vn",
             address="Cầu Giấy, Hà Nội"),
    Supplier(supplier_id=5, name="Logitech VN", contact_name="Hoàng Văn E",
             phone="0905678901", email="logitech@supplier.vn",
             address="Thanh Xuân, Hà Nội"),
]

SUP_MAP: Dict[int, Supplier] = {s.supplier_id: s for s in SUPPLIERS}


# ══════════════════════════════════════════════════════════════
# PRODUCTS  (20 realistic tech products)
# ══════════════════════════════════════════════════════════════
def _img(name: str) -> str:
    """Return an absolute path from the static mount root.

    Templates render these in <img src="..."> tags.
    The FastAPI StaticFiles mount is at /static, so paths start from there.
    """
    return f"/static/images/products/{name}"

PRODUCTS: List[Product] = [
    Product(
        product_id=1, name="iPhone 15 Pro Max", is_new=True, is_hot=True, rating=4.9,
        description="iPhone 15 Pro Max với chip A17 Pro, camera 48MP, màn hình Super Retina XDR 6.7 inch.",
        price=34990000, original_price=39990000, discount_percent=13,
        stock_quantity=45, category=CAT_MAP[1], supplier=SUP_MAP[1],
        image_url=_img("iPhone_15_Pro_Max.png"),
        images=[_img("iPhone_15_Pro_Max.png"), _img("iPhone_15_Pro_Max.png")],
        variants=[
            ProductVariant(variant_id=1, color="Titan Tự nhiên", storage="256GB", price=34990000),
            ProductVariant(variant_id=2, color="Titan Xanh", storage="512GB", price=39990000),
            ProductVariant(variant_id=3, color="Titan Đen", storage="1TB", price=44990000),
        ]
    ),
    Product(
        product_id=2, name="Samsung Galaxy S24 Ultra", is_new=True, is_hot=True, rating=4.8,
        description="Galaxy S24 Ultra với S Pen tích hợp, camera 200MP, màn hình Dynamic AMOLED 2X 6.8 inch.",
        price=29990000, original_price=32990000, discount_percent=9,
        stock_quantity=38, category=CAT_MAP[1], supplier=SUP_MAP[2],
        image_url=_img("Galaxy_S24_Ultra.png"),
        images=[_img("Galaxy_S24_Ultra.png")],
        variants=[
            ProductVariant(variant_id=4, color="Titan Đen", storage="256GB", price=29990000),
            ProductVariant(variant_id=5, color="Titan Vàng", storage="512GB", price=32990000),
        ]
    ),
    Product(
        product_id=3, name="MacBook Pro 14 M3 Pro", is_new=True, rating=4.9,
        description="MacBook Pro 14 inch với chip M3 Pro, 18GB RAM, màn hình Liquid Retina XDR.",
        price=47990000, stock_quantity=22, category=CAT_MAP[2], supplier=SUP_MAP[1],
        image_url=_img("MacBook_Pro_14_M3_Pro.png"),
        images=[_img("MacBook_Pro_14_M3_Pro.png")],
        variants=[
            ProductVariant(variant_id=6, color="Bạc", storage="512GB", price=47990000),
            ProductVariant(variant_id=7, color="Space Black", storage="1TB", price=57990000),
        ]
    ),
    Product(
        product_id=4, name="MacBook Air M3", is_new=True, rating=4.7,
        description="MacBook Air M3 13 inch siêu mỏng nhẹ, chip Apple M3, 8-core GPU.",
        price=28990000, stock_quantity=30, category=CAT_MAP[2], supplier=SUP_MAP[1],
        image_url=_img("MacBook_Air_M3.png"),
        images=[_img("MacBook_Air_M3.png")],
        variants=[
            ProductVariant(variant_id=8, color="Bạc", storage="256GB", price=28990000),
            ProductVariant(variant_id=9, color="Space Gray", storage="512GB", price=33990000),
        ]
    ),
    Product(
        product_id=5, name="Dell XPS 15", is_hot=True, rating=4.6,
        description="Dell XPS 15 với Intel Core i9 thế hệ 13, RAM 32GB, màn hình OLED 3.5K.",
        price=54990000, stock_quantity=15, category=CAT_MAP[2], supplier=SUP_MAP[5],
        image_url=_img("Dell_XPS_15.png"),
        images=[_img("Dell_XPS_15.png")],
        variants=[
            ProductVariant(variant_id=10, color="Platinum Silver", storage="1TB", price=54990000),
        ]
    ),
    Product(
        product_id=6, name="HP Pavilion Plus 14", rating=4.5,
        description="HP Pavilion Plus 14 với Intel Core i7, màn hình 2.8K OLED, thiết kế mỏng nhẹ.",
        price=24990000, stock_quantity=28, category=CAT_MAP[2], supplier=SUP_MAP[5],
        image_url=_img("HP_Pavilion_Plus_14.png"),
        images=[_img("HP_Pavilion_Plus_14.png")],
        variants=[
            ProductVariant(variant_id=11, color="Bạc", storage="512GB", price=24990000),
            ProductVariant(variant_id=12, color="Vàng", storage="1TB", price=29990000),
        ]
    ),
    Product(
        product_id=7, name="AirPods Pro 2", is_hot=True, rating=4.8,
        description="AirPods Pro 2 với chống ồn chủ động, sạc USB-C, pin 6 giờ.",
        price=6490000, original_price=7490000, discount_percent=13,
        stock_quantity=60, category=CAT_MAP[4], supplier=SUP_MAP[1],
        image_url=_img("AirPods_Pro_2.png"),
        images=[_img("AirPods_Pro_2.png"), _img("AirPods_Pro_2__01.jpg")],
        variants=[
            ProductVariant(variant_id=13, color="Trắng", storage="USB-C", price=6490000),
        ]
    ),
    Product(
        product_id=8, name="Sony WH-1000XM5", rating=4.9,
        description="Tai nghe chụp tai Sony WH-1000XM5 với chống ồn tốt nhất, pin 30 giờ.",
        price=8990000, original_price=9990000, discount_percent=10,
        stock_quantity=35, category=CAT_MAP[4], supplier=SUP_MAP[5],
        image_url=_img("Sony_WH-1000XM5.png"),
        images=[_img("Sony_WH-1000XM5.png")],
        variants=[
            ProductVariant(variant_id=14, color="Đen", storage="30h", price=8990000),
            ProductVariant(variant_id=15, color="Bạc", storage="30h", price=8990000),
        ]
    ),
    Product(
        product_id=9, name="Samsung Galaxy Tab S9 Ultra", is_new=True, rating=4.7,
        description="Tablet Samsung Galaxy Tab S9 Ultra 14.6 inch, S Pen, chống nước IP68.",
        price=26990000, stock_quantity=20, category=CAT_MAP[3], supplier=SUP_MAP[2],
        image_url=_img("Tab_S9_Ultra.png"),
        images=[_img("Tab_S9_Ultra.png")],
        variants=[
            ProductVariant(variant_id=16, color="Đen", storage="256GB", price=26990000),
            ProductVariant(variant_id=17, color="Bạc", storage="512GB", price=29990000),
        ]
    ),
    Product(
        product_id=10, name="iPad Air M2", is_new=True, rating=4.8,
        description="iPad Air M2 11 inch với chip Apple M2, hỗ trợ Apple Pencil Pro.",
        price=18990000, stock_quantity=25, category=CAT_MAP[3], supplier=SUP_MAP[1],
        image_url=_img("iPad_Air_M2.png"),
        images=[_img("iPad_Air_M2.png")],
        variants=[
            ProductVariant(variant_id=18, color="Space Gray", storage="128GB", price=18990000),
            ProductVariant(variant_id=19, color="Starlight", storage="256GB", price=21990000),
        ]
    ),
    Product(
        product_id=11, name="Anker 735 GaNPrime 65W", rating=4.6,
        description="Sạc nhanh GaN 65W đa cổng, sạc được laptop và điện thoại.",
        price=1490000, original_price=1990000, discount_percent=25,
        stock_quantity=80, category=CAT_MAP[6], supplier=SUP_MAP[4],
        image_url=_img("Anker_735_65W.png"),
        images=[_img("Anker_735_65W.png")],
        variants=[
            ProductVariant(variant_id=20, color="Đen", storage="65W", price=1490000),
        ]
    ),
    Product(
        product_id=12, name="HyperDrive Gen2 Hub", rating=4.5,
        description="USB-C Hub 7 in 1, HDMI 4K, SD card reader, USB-A, PD 100W.",
        price=2190000, stock_quantity=50, category=CAT_MAP[6], supplier=SUP_MAP[4],
        image_url=_img("HyperDrive_Gen2.png"),
        images=[_img("HyperDrive_Gen2.png")],
        variants=[
            ProductVariant(variant_id=21, color="Space Gray", storage="7-in-1", price=2190000),
        ]
    ),
    Product(
        product_id=13, name="Logitech MX Master 3S", is_hot=True, rating=4.8,
        description="Chuột không dây cao cấp MX Master 3S, cuộn MagSpeed, cảm biến 8000 DPI.",
        price=3290000, original_price=3990000, discount_percent=18,
        stock_quantity=55, category=CAT_MAP[8], supplier=SUP_MAP[5],
        image_url=_img("MX_Master_3S.png"),
        images=[_img("MX_Master_3S.png")],
        variants=[
            ProductVariant(variant_id=22, color="Đen", storage="8000 DPI", price=3290000),
            ProductVariant(variant_id=23, color="Trắng", storage="8000 DPI", price=3290000),
        ]
    ),
    Product(
        product_id=14, name="Keychron K3 Pro", rating=4.5,
        description="Bàn phím cơ siêu mỏng Keychron K3 Pro 75%, switch low-profile.",
        price=2490000, stock_quantity=40, category=CAT_MAP[8], supplier=SUP_MAP[5],
        image_url=_img("Keychron_K3_Pro.png"),
        images=[_img("Keychron_K3_Pro.png")],
        variants=[
            ProductVariant(variant_id=24, color="Đen", storage="K3 Pro Brown", price=2490000),
            ProductVariant(variant_id=25, color="Trắng", storage="K3 Pro Blue", price=2490000),
        ]
    ),
    Product(
        product_id=15, name="Samsung Galaxy A55 5G", is_new=True, rating=4.4,
        description="Samsung Galaxy A55 5G với màn hình Super AMOLED 6.6 inch, camera 50MP.",
        price=10990000, stock_quantity=48, category=CAT_MAP[1], supplier=SUP_MAP[2],
        image_url=_img("Galaxy_A55_5G.png"),
        images=[_img("Galaxy_A55_5G.png")],
        variants=[
            ProductVariant(variant_id=26, color="Đen", storage="256GB", price=10990000),
            ProductVariant(variant_id=27, color="Tím nhạt", storage="256GB", price=10990000),
        ]
    ),
    Product(
        product_id=16, name="Xiaomi 13T Pro", is_new=True, rating=4.5,
        description="Xiaomi 13T Pro với Leica camera, chip Dimensity 9200+, sạc 120W.",
        price=13990000, original_price=15990000, discount_percent=13,
        stock_quantity=33, category=CAT_MAP[1], supplier=SUP_MAP[3],
        image_url=_img("Xiaomi_13T_Pro.png"),
        images=[_img("Xiaomi_13T_Pro.png")],
        variants=[
            ProductVariant(variant_id=28, color="Đen", storage="512GB", price=13990000),
        ]
    ),
    Product(
        product_id=17, name="ROG Zephyrus G14", is_hot=True, rating=4.7,
        description="Laptop gaming ASUS ROG Zephyrus G14 với AMD Ryzen 9, RTX 4070, màn hình 165Hz.",
        price=44990000, stock_quantity=18, category=CAT_MAP[2], supplier=SUP_MAP[5],
        image_url=_img("ROG_Zephyrus_G14.png"),
        images=[_img("ROG_Zephyrus_G14.png")],
        variants=[
            ProductVariant(variant_id=29, color="Đen", storage="1TB", price=44990000),
        ]
    ),
    Product(
        product_id=18, name="Galaxy Watch 6 Classic", rating=4.6,
        description="Samsung Galaxy Watch 6 Classic 47mm với viền xoay, theo dõi sức khỏe toàn diện.",
        price=8990000, original_price=9990000, discount_percent=10,
        stock_quantity=30, category=CAT_MAP[5], supplier=SUP_MAP[2],
        image_url=_img("Galaxy_Watch_6_Classic.png"),
        images=[_img("Galaxy_Watch_6_Classic.png")],
        variants=[
            ProductVariant(variant_id=30, color="Đen", storage="47mm", price=8990000),
            ProductVariant(variant_id=31, color="Bạc", storage="47mm", price=8990000),
        ]
    ),
    Product(
        product_id=19, name="iPhone 14", rating=4.6,
        description="iPhone 14 với chip A15 Bionic, camera 12MP, màn hình Super Retina 6.1 inch.",
        price=19990000, stock_quantity=42, category=CAT_MAP[1], supplier=SUP_MAP[1],
        image_url=_img("iPhone_14.png"),
        images=[_img("iPhone_14.png")],
        variants=[
            ProductVariant(variant_id=32, color="Đen", storage="128GB", price=19990000),
            ProductVariant(variant_id=33, color="Tím", storage="256GB", price=22990000),
        ]
    ),
    Product(
        product_id=20, name="Corsair K70 RGB Pro", rating=4.7,
        description="Bàn phím cơ Corsair K70 RGB Pro với switch Cherry MX, RGB per-key.",
        price=4490000, stock_quantity=36, category=CAT_MAP[8], supplier=SUP_MAP[5],
        image_url=_img("Corsair_K70_RGB_Pro.png"),
        images=[_img("Corsair_K70_RGB_Pro.png")],
        variants=[
            ProductVariant(variant_id=34, color="Đen", storage="CHERRY MX Red", price=4490000),
        ]
    ),
]

PRODUCT_MAP: Dict[int, Product] = {p.product_id: p for p in PRODUCTS}


# ══════════════════════════════════════════════════════════════
# ACCOUNTS
# ══════════════════════════════════════════════════════════════
ACCOUNTS: List[Account] = [
    Account(account_id=1, username="admin", email="admin@webstore.vn",
            full_name="Nguyễn Quản Trị", role="Admin",
            created_at=datetime(2024, 1, 1)),
    Account(account_id=2, username="employee01", email="nv01@webstore.vn",
            full_name="Trần Nhân Viên", role="Employee",
            created_at=datetime(2024, 2, 15)),
    Account(account_id=3, username="customer1", email="khach1@email.com",
            full_name="Lê Khách Hàng", role="Customer",
            created_at=datetime(2024, 3, 10)),
    Account(account_id=4, username="customer2", email="khach2@email.com",
            full_name="Phạm Mua Hàng", role="Customer",
            created_at=datetime(2024, 4, 20)),
]

ACCOUNT_MAP: Dict[str, Account] = {a.username: a for a in ACCOUNTS}

# Demo credentials: username → password (plaintext for demo only)
DEMO_PASSWORDS = {
    "admin": "admin123",
    "employee01": "employee123",
    "customer1": "customer123",
    "customer2": "customer123",
}


# ══════════════════════════════════════════════════════════════
# ORDERS
# ══════════════════════════════════════════════════════════════
def _make_order(order_id: int, customer: str, status: str,
                days_ago: int, items: List[CartItem]) -> Order:
    total = sum(
        (item.variant.price if item.variant else (item.product.price if item.product else 0)) * item.quantity
        for item in items
    )
    return Order(
        order_id=order_id, customer_name=customer,
        customer_email=f"{customer.lower().replace(' ', '')}@email.com",
        customer_phone="0901234567",
        shipping_address="Đường Trịnh Văn Bô, Xuân Phương, Nam Từ Liêm, Hà Nội",
        status=status, order_date=datetime.now() - timedelta(days=days_ago),
        items=items, total_amount=total,
    )


_order_items_1 = [
    CartItem(product_id=1, quantity=1, product=PRODUCT_MAP[1],
             variant=PRODUCT_MAP[1].variants[0]),
    CartItem(product_id=7, quantity=2, product=PRODUCT_MAP[7],
             variant=PRODUCT_MAP[7].variants[0]),
]
_order_items_2 = [
    CartItem(product_id=3, quantity=1, product=PRODUCT_MAP[3],
             variant=PRODUCT_MAP[3].variants[0]),
]
_order_items_3 = [
    CartItem(product_id=13, quantity=1, product=PRODUCT_MAP[13],
             variant=PRODUCT_MAP[13].variants[0]),
    CartItem(product_id=14, quantity=1, product=PRODUCT_MAP[14],
             variant=PRODUCT_MAP[14].variants[0]),
]
_order_items_4 = [
    CartItem(product_id=9, quantity=1, product=PRODUCT_MAP[9],
             variant=PRODUCT_MAP[9].variants[0]),
]

ORDERS: List[Order] = [
    _make_order(1001, "Lê Khách Hàng", "Completed", 1, _order_items_1),
    _make_order(1002, "Phạm Mua Hàng", "Processing", 2, _order_items_2),
    _make_order(1003, "Lê Khách Hàng", "New", 3, _order_items_3),
    _make_order(1004, "Trần Mua Hàng", "Canceled", 5, _order_items_4),
    _make_order(1005, "Nguyễn Tester", "New", 0, []),
    _make_order(1006, "Võ Khách", "Processing", 1, []),
]

ORDER_MAP: Dict[int, Order] = {o.order_id: o for o in ORDERS}


# ══════════════════════════════════════════════════════════════
# SERVICE FUNCTIONS
# ══════════════════════════════════════════════════════════════

def get_all_products() -> List[Product]:
    return PRODUCTS


def get_product_by_id(product_id: int) -> Optional[Product]:
    return PRODUCT_MAP.get(product_id)


def get_products_by_category(category_id: int) -> List[Product]:
    return [p for p in PRODUCTS if p.category and p.category.category_id == category_id]


def get_new_products() -> List[Product]:
    return [p for p in PRODUCTS if p.is_new]


def get_hot_products() -> List[Product]:
    return [p for p in PRODUCTS if p.is_hot]


def search_products(query: str) -> List[Product]:
    q = query.lower()
    return [p for p in PRODUCTS if q in p.name.lower() or q in p.description.lower()]


def paginate_products(
    products: List[Product],
    page: int = 1,
    page_size: int = 8,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "newest",
) -> PaginatedProducts:
    filtered = products

    if search:
        q = search.lower()
        filtered = [p for p in filtered
                    if q in p.name.lower() or q in (p.description or "").lower()]
    if category_id:
        filtered = [p for p in filtered
                    if p.category and p.category.category_id == category_id]
    if min_price is not None:
        filtered = [p for p in filtered if p.price >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p.price <= max_price]

    if sort_by == "price_asc":
        filtered = sorted(filtered, key=lambda p: p.price)
    elif sort_by == "price_desc":
        filtered = sorted(filtered, key=lambda p: p.price, reverse=True)
    elif sort_by == "name_asc":
        filtered = sorted(filtered, key=lambda p: p.name)
    # "newest" keeps original order (is_new first, then is_hot)

    total = len(filtered)
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    items = filtered[start:start + page_size]

    return PaginatedProducts(
        items=items, total_count=total,
        current_page=page, total_pages=total_pages,
        has_previous=page > 1,
        has_next=page < total_pages,
    )


def get_all_categories() -> List[Category]:
    return CATEGORIES


def get_all_suppliers() -> List[Supplier]:
    return SUPPLIERS


def get_supplier_by_id(supplier_id: int) -> Optional[Supplier]:
    return SUP_MAP.get(supplier_id)


def get_all_accounts() -> List[Account]:
    return ACCOUNTS


def get_account_by_username(username: str) -> Optional[Account]:
    return ACCOUNT_MAP.get(username)


def validate_credentials(username: str, password: str) -> bool:
    return DEMO_PASSWORDS.get(username) == password


def authenticate(username: str, password: str) -> Optional[Account]:
    if validate_credentials(username, password):
        return ACCOUNT_MAP.get(username)
    return None


def get_all_orders() -> List[Order]:
    return ORDERS


def get_order_by_id(order_id: int) -> Optional[Order]:
    return ORDER_MAP.get(order_id)


def get_dashboard_stats() -> StatisticsViewModel:
    today = datetime.now().date()
    week_ago = today - timedelta(days=6)

    # Revenue by day (last 7 days)
    revenue_by_day = [
        RevenueDay(
            date=(week_ago + timedelta(days=i)).strftime("%d/%m"),
            revenue=random.uniform(5_000_000, 25_000_000),
        )
        for i in range(7)
    ]

    return StatisticsViewModel(
        total_orders=len(ORDERS),
        today_orders=random.randint(1, 5),
        total_revenue=sum(r.revenue for r in revenue_by_day) * 10,
        today_revenue=random.uniform(3_000_000, 15_000_000),
        total_stock=sum(p.stock_quantity for p in PRODUCTS),
        pending_orders=random.randint(2, 8),
        account_count=len(ACCOUNTS),
        new_orders=random.randint(1, 4),
        processing_orders=random.randint(3, 7),
        delivered_orders=random.randint(10, 20),
        canceled_orders=random.randint(1, 3),
        top_products=[
            TopProduct(product_id=1, product_name=p.name,
                       image_url=p.image_url,
                       total_sold=random.randint(20, 150),
                       total_revenue=random.uniform(500_000_000, 3_000_000_000))
            for p in PRODUCTS[:5]
        ],
        recent_orders=[
            RecentOrder(order_id=o.order_id, customer_name=o.customer_name,
                        order_date=o.order_date, status=o.status)
            for o in sorted(ORDERS, key=lambda x: x.order_date, reverse=True)[:5]
        ],
        revenue_by_day=revenue_by_day,
    )
