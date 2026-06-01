"""
Product Model - Sản phẩm
Tương đương Models/Product.cs trong C#
"""
import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base

# ── Image URL normalization helpers ──────────────────────────────────────────

def _image_file_exists(static_url: str) -> bool:
    if not static_url:
        return False
    filename = static_url.lstrip("/").replace("static/", "", 1)
    full_path = os.path.join(os.path.dirname(__file__), os.pardir, "wwwroot",
                             filename.replace("/", os.sep))
    return os.path.isfile(full_path)

def _normalize_image_url(url: str) -> str:
    """Chuẩn hóa URL ảnh — dùng chung cho Product và ProductImage.

    Chuẩn duy nhất: /static/images/products/
    Hỗ trợ legacy: /images/... (prepend /static/)
    Tất cả ảnh upload mới: /static/images/products/... (trả ngay, không check file)
    """
    if not url:
        return "/static/images/no-image.png"

    # URL đã đúng format hoặc full URL → trả ngay
    if url.startswith("http://") or url.startswith("https://") or url.startswith("/static/"):
        return url

    # Legacy: /images/... → /static/images/...
    if url.startswith("/images/"):
        return "/static" + url

    # Fallback
    return url

# ── Debug logging ─────────────────────────────────────────────────────────────

_LOG_PATH = os.path.join(os.path.dirname(__file__), os.pardir, "debug-ed9600.log")

def _debug_log(session_id: str, hypothesis_id: str, location: str, message: str, data: dict):
    try:
        import json, time
        log_entry = {
            "sessionId": session_id, "id": f"log_{int(time.time()*1000)}",
            "timestamp": int(time.time()*1000), "location": location,
            "message": message, "data": data, "hypothesisId": hypothesis_id
        }
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


class Product(Base):
    __tablename__ = "Products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    image_url = Column(String(500))
    price = Column(DECIMAL(10, 2), nullable=False)
    original_price = Column(DECIMAL(10, 2))
    stock_quantity = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    rating = Column(DECIMAL(2, 1), default=4.5)
    is_new = Column(Boolean, default=False)
    is_hot = Column(Boolean, default=False)
    discount_percent = Column(Integer, default=0)
    specifications = Column(Text)
    category_id = Column(Integer, ForeignKey("Categories.category_id"))
    supplier_id = Column(Integer, ForeignKey("Suppliers.supplier_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Helper: chuẩn hóa URL ảnh — prepend /static/ nếu DB lưu /images/
    @staticmethod
    def _normalize(url: str) -> str:
        return _normalize_image_url(url)

    @property
    def image_url_normalized(self) -> str:
        """Dùng trong template: trả về URL có /static/ prefix, tự tìm file đúng"""
        return _normalize_image_url(self.__dict__.get('image_url'))

    @property
    def is_deal(self) -> bool:
        return self.discount_percent > 0 or (
            self.original_price is not None and self.original_price > self.price
        )

    @property
    def first_image_url(self) -> str:
        """Lấy URL ảnh đầu tiên cho sản phẩm.

        Ưu tiên:
        1. product.image_url (đã normalized)
        2. Ảnh đầu tiên trong ProductImages table (variant_id=None, is_primary=True)
        3. Ảnh đầu tiên bất kỳ trong ProductImages table
        4. Fallback: no-image.png
        """
        # Ưu tiên 1: image_url của product
        url = self.__dict__.get('image_url')
        if url:
            return _normalize_image_url(url)

        # Ưu tiên 2: Lấy từ ProductImages (lazy load)
        try:
            imgs = self.product_images
            if imgs:
                # Tìm ảnh chính trước (is_primary=True)
                primary = [i for i in imgs if getattr(i, 'is_primary', False)]
                if primary:
                    return _normalize_image_url(primary[0].image_url)
                # Tìm ảnh không thuộc variant nào (variant_id=None)
                no_variant = [i for i in imgs if not getattr(i, 'variant_id', None)]
                if no_variant:
                    return _normalize_image_url(no_variant[0].image_url)
                # Lấy ảnh đầu tiên bất kỳ
                return _normalize_image_url(imgs[0].image_url)
        except Exception:
            pass

        # Fallback
        return "/static/images/no-image.png"

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    product_images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    receipt_shipments = relationship("ReceiptShipment", back_populates="product")

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"


class ProductVariant(Base):
    __tablename__ = "ProductVariants"

    variant_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False)
    color = Column(String(50))
    color_hex = Column(String(7))
    storage = Column(String(20))
    ram = Column(String(20))
    variant_name = Column(String(100))
    sku = Column(String(50))
    price = Column(DECIMAL(10, 2))
    original_price = Column(DECIMAL(10, 2))
    stock_quantity = Column(Integer, default=0)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="variants")
    product_images = relationship("ProductImage", back_populates="variant", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="variant")
    cart_items = relationship("CartItem", back_populates="variant")

    def __repr__(self):
        return f"<ProductVariant(name='{self.variant_name}')>"


class ProductImage(Base):
    __tablename__ = "ProductImages"

    image_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("ProductVariants.variant_id"), nullable=True)
    image_url = Column(String(500), nullable=False)
    display_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="product_images")
    variant = relationship("ProductVariant", back_populates="product_images")

    @property
    def image_url_normalized(self) -> str:
        """Chuẩn hóa URL ảnh — dùng chung logic với Product"""
        return _normalize_image_url(self.__dict__.get('image_url'))

    def __repr__(self):
        return f"<ProductImage(product_id={self.product_id})>"
