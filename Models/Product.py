"""
Product Model - Sản phẩm
Tương đương Models/Product.cs trong C#
"""
from sqlalchemy import Column, Integer, String, Unicode, UnicodeText, Boolean, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class Product(Base):
    __tablename__ = "Products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255), nullable=False, index=True)
    description = Column(UnicodeText)
    image_url = Column(Unicode(500))
    price = Column(DECIMAL(10, 2), nullable=False)
    original_price = Column(DECIMAL(10, 2))
    stock_quantity = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    rating = Column(DECIMAL(2, 1), default=4.5)
    is_new = Column(Boolean, default=False)
    is_hot = Column(Boolean, default=False)
    discount_percent = Column(Integer, default=0)
    specifications = Column(UnicodeText)  # JSON string cho thông số kỹ thuật
    category_id = Column(Integer, ForeignKey("Categories.category_id"))
    supplier_id = Column(Integer, ForeignKey("Suppliers.supplier_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Computed property (không lưu DB)
    @property
    def is_deal(self) -> bool:
        return self.discount_percent > 0 or (
            self.original_price is not None and self.original_price > self.price
        )

    @property
    def first_image_url(self) -> str:
        """Lấy ảnh đầu tiên: ưu tiên primary, không thì theo display_order, fallback sang image_url gốc"""
        if self.product_images:
            for img in sorted(self.product_images, key=lambda x: (not x.is_primary, x.display_order)):
                if img.image_url:
                    return img.image_url
        return self.image_url or "/static/images/no-image.png"

    # Relationships
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


"""
ProductVariant Model - Biến thể sản phẩm
Tương đương Models/ProductVariant.cs trong C#
"""


class ProductVariant(Base):
    __tablename__ = "ProductVariants"

    variant_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False)
    color = Column(Unicode(50))
    color_hex = Column(String(7))  # Mã màu hex cho swatch (VD: #FF5733)
    storage = Column(Unicode(20))
    ram = Column(Unicode(20))
    variant_name = Column(Unicode(100))
    sku = Column(Unicode(50))
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


"""
ProductImage Model - Hình ảnh sản phẩm
Tương đương Models/ProductImage.cs trong C#
"""


class ProductImage(Base):
    __tablename__ = "ProductImages"

    image_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("ProductVariants.variant_id"), nullable=True)
    image_url = Column(Unicode(500), nullable=False)
    display_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="product_images")
    variant = relationship("ProductVariant", back_populates="variant_images")

    def __repr__(self):
        return f"<ProductImage(product_id={self.product_id})>"
