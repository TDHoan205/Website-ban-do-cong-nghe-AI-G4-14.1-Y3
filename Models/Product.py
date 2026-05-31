"""
Product Model - Sản phẩm
Tương đương Models/Product.cs trong C#
"""
import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base

_LOG_PATH = os.path.join(os.path.dirname(__file__), os.pardir, "debug-ed9600.log")

def _debug_log(session_id: str, hypothesis_id: str, location: str, message: str, data: dict):
    try:
        import json, time
        log_entry = {
            "sessionId": session_id,
            "id": f"log_{int(time.time() * 1000)}",
            "timestamp": int(time.time() * 1000),
            "location": location,
            "message": message,
            "data": data,
            "hypothesisId": hypothesis_id
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

    @property
    def is_deal(self) -> bool:
        return self.discount_percent > 0 or (
            self.original_price is not None and self.original_price > self.price
        )

    @property
    def first_image_url(self) -> str:
        images = self.product_images
        _debug_log("ed9600", "H2", "Product.first_image_url",
            "first_image_url called",
            {
                "product_id": self.product_id,
                "name": self.name[:40] if self.name else "",
                "product_images_count": len(images) if images else 0,
                "product_images": [
                    {"image_id": i.image_id, "image_url": i.image_url, "is_primary": bool(i.is_primary), "display_order": i.display_order}
                    for i in (images or [])
                ] if images else [],
                "product_image_url": self.image_url or ""
            })

        def _static(url):
            if url and url.startswith("/images/"):
                return "/static" + url
            return url or "/static/images/no-image.png"

        if images:
            sorted_imgs = sorted(images, key=lambda x: (not x.is_primary, x.display_order))
            for img in sorted_imgs:
                if img.image_url:
                    _debug_log("ed9600", "H2", "Product.first_image_url:selected",
                        "first_image_url: selected image",
                        {"selected_image_id": img.image_id, "image_url": img.image_url, "is_primary": bool(img.is_primary)})
                    return _static(img.image_url)
        fallback = _static(self.image_url)
        _debug_log("ed9600", "H2", "Product.first_image_url:fallback",
            "first_image_url: using fallback",
            {"fallback_url": fallback, "product_image_url": self.image_url or ""})
        return fallback

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
    variant_images = relationship("ProductImage", back_populates="variant", cascade="all, delete-orphan")
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
    variant = relationship("ProductVariant", back_populates="variant_images")

    def __repr__(self):
        return f"<ProductImage(product_id={self.product_id})>"
