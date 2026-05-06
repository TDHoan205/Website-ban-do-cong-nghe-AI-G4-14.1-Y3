"""
Cart Model - Giỏ hàng
Tương đương Models/Cart.cs trong C#
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class Cart(Base):
    __tablename__ = "Carts"

    cart_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("Accounts.account_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    account = relationship("Account", back_populates="carts")
    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.cart_items)

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.cart_items)

    def __repr__(self):
        return f"<Cart(account_id={self.account_id}, items={self.total_items})>"


"""
CartItem Model - Item trong giỏ hàng
Tương đương Models/CartItem.cs trong C#
"""


class CartItem(Base):
    __tablename__ = "CartItems"

    cart_item_id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("Carts.cart_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("ProductVariants.variant_id"), nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    added_date = Column(DateTime(timezone=True), server_default=func.now())

    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    variant = relationship("ProductVariant", back_populates="cart_items")

    @property
    def unit_price(self) -> float:
        if self.variant and self.variant.price:
            return float(self.variant.price)
        return float(self.product.price) if self.product else 0

    @property
    def subtotal(self) -> float:
        return self.unit_price * self.quantity

    def __repr__(self):
        return f"<CartItem(product_id={self.product_id}, qty={self.quantity})>"
