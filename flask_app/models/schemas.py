from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime


# ─── Product ───────────────────────────────────────────────
class ProductVariant(BaseModel):
    variant_id: int
    color: str
    storage: str
    price: float
    image_url: Optional[str] = None


class ProductCategory(BaseModel):
    category_id: int
    name: str


class ProductSupplier(BaseModel):
    supplier_id: int
    name: str


class Product(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    product_id: int
    name: str
    description: str
    price: float
    original_price: Optional[float] = None
    discount_percent: int = 0
    image_url: Optional[str] = None
    images: List[str] = []
    stock_quantity: int = 50
    is_available: bool = True
    is_new: bool = False
    is_hot: bool = False
    rating: float = 0.0
    category: Any = None
    supplier: Any = None
    variants: List[ProductVariant] = []


# ─── Cart ─────────────────────────────────────────────────
class CartItem(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    product: Optional[Product] = None
    variant: Optional[ProductVariant] = None
    quantity: int = 1


# ─── Order ────────────────────────────────────────────────
class Order(BaseModel):
    order_id: int
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    status: str
    order_date: datetime
    items: List[CartItem] = []
    total_amount: float


# ─── Account / User ───────────────────────────────────────
class Account(BaseModel):
    account_id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool = True
    created_at: datetime


# ─── Category ─────────────────────────────────────────────
class Category(BaseModel):
    category_id: int
    name: str
    description: str = ""


# ─── Supplier ──────────────────────────────────────────────
class Supplier(BaseModel):
    supplier_id: int
    name: str
    contact_name: str
    phone: str
    email: str
    address: str


# ─── Dashboard Stats ──────────────────────────────────────
class RevenueDay(BaseModel):
    date: str
    revenue: float


class TopProduct(BaseModel):
    product_id: int
    product_name: str
    image_url: Optional[str]
    total_sold: int
    total_revenue: float


class RecentOrder(BaseModel):
    order_id: int
    customer_name: str
    order_date: datetime
    status: str


class StatisticsViewModel(BaseModel):
    total_orders: int
    today_orders: int
    total_revenue: float
    today_revenue: float
    total_stock: int
    pending_orders: int
    account_count: int
    new_orders: int
    processing_orders: int
    delivered_orders: int
    canceled_orders: int
    top_products: List[TopProduct]
    recent_orders: List[RecentOrder]
    revenue_by_day: List[RevenueDay]


# ─── Pagination ────────────────────────────────────────────
class PaginatedProducts(BaseModel):
    items: List[Product]
    total_count: int
    current_page: int
    total_pages: int
    has_previous: bool
    has_next: bool
