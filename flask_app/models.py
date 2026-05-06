"""
SQLAlchemy ORM models – mirrors the SQL Server TechShopWebsite2 schema.
Every model maps 1:1 to its database table.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text,
    ForeignKey, DECIMAL, BigInteger, UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

try:
    from flask_app.database import Base
except ModuleNotFoundError:
    from database import Base


# ═══════════════════════════════════════════════════════════════════════════════
# Role / Auth
# ═══════════════════════════════════════════════════════════════════════════════

class Role(Base):
    __tablename__ = "Roles"

    role_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    permissions: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)  # JSON
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="role")


# ═══════════════════════════════════════════════════════════════════════════════
# Account / User
# ═══════════════════════════════════════════════════════════════════════════════

class Account(Base):
    __tablename__ = "Accounts"

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("Roles.role_id"), nullable=False)
    reset_token: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    reset_token_expiry: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    role: Mapped["Role"] = relationship("Role", back_populates="accounts")
    cart: Mapped[Optional["Cart"]] = relationship("Cart", back_populates="account", uselist=False)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="account")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="account")


class Employee(Base):
    __tablename__ = "Employees"

    employee_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("Accounts.account_id"), unique=True, nullable=False)
    department: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    position: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    hire_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    salary: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    account: Mapped["Account"] = relationship("Account")


# ═══════════════════════════════════════════════════════════════════════════════
# Category / Product
# ═══════════════════════════════════════════════════════════════════════════════

class Category(Base):
    __tablename__ = "Categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")


class Supplier(Base):
    __tablename__ = "Suppliers"

    supplier_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_person: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())

    products: Mapped[List["Product"]] = relationship("Product", back_populates="supplier")


class Product(Base):
    __tablename__ = "Products"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    original_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    rating: Mapped[Decimal] = mapped_column(DECIMAL(2, 1), default=Decimal("4.5"))
    is_new: Mapped[bool] = mapped_column(Boolean, default=False)
    is_hot: Mapped[bool] = mapped_column(Boolean, default=False)
    discount_percent: Mapped[int] = mapped_column(Integer, default=0)
    specifications: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Categories.category_id"), nullable=True)
    supplier_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Suppliers.supplier_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())

    # Relationships
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="products")
    supplier: Mapped[Optional["Supplier"]] = relationship("Supplier", back_populates="products")
    variants: Mapped[List["ProductVariant"]] = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    images: Mapped[List["ProductImage"]] = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    cart_items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="product")


class ProductVariant(Base):
    __tablename__ = "ProductVariants"

    variant_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("Products.product_id", ondelete="CASCADE"), nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    storage: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    ram: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    variant_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sku: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    original_price: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    product: Mapped["Product"] = relationship("Product", back_populates="variants")
    cart_items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="variant")


class ProductImage(Base):
    __tablename__ = "ProductImages"

    image_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("Products.product_id", ondelete="CASCADE"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    product: Mapped["Product"] = relationship("Product", back_populates="images")


class Inventory(Base):
    __tablename__ = "Inventory"

    inventory_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("Products.product_id"), unique=True, nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, default=0)
    min_stock_level: Mapped[int] = mapped_column(Integer, default=5)
    max_stock_level: Mapped[int] = mapped_column(Integer, default=100)
    last_restock_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())

    product: Mapped["Product"] = relationship("Product")


# ═══════════════════════════════════════════════════════════════════════════════
# Cart
# ═══════════════════════════════════════════════════════════════════════════════

class Cart(Base):
    __tablename__ = "Carts"

    cart_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("Accounts.account_id"), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())

    account: Mapped["Account"] = relationship("Account", back_populates="cart")
    items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "CartItems"

    cart_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("Carts.cart_id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("Products.product_id"), nullable=False)
    variant_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ProductVariants.variant_id"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    added_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")
    variant: Mapped[Optional["ProductVariant"]] = relationship("ProductVariant", back_populates="cart_items")


# ═══════════════════════════════════════════════════════════════════════════════
# Order
# ═══════════════════════════════════════════════════════════════════════════════

class Order(Base):
    __tablename__ = "Orders"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Pending")
    customer_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    customer_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    customer_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())

    account: Mapped[Optional["Account"]] = relationship("Account", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "OrderItems"

    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("Orders.order_id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("Products.product_id"), nullable=False)
    variant_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("ProductVariants.variant_id"), nullable=True)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    variant_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")
    variant: Mapped[Optional["ProductVariant"]] = relationship("ProductVariant")


# ═══════════════════════════════════════════════════════════════════════════════
# Chat / AI
# ═══════════════════════════════════════════════════════════════════════════════

class ChatSession(Base):
    __tablename__ = "ChatSessions"

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_uuid: Mapped[str] = mapped_column(String(36), unique=True, nullable=False)
    account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    device_info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    account: Mapped[Optional["Account"]] = relationship("Account")
    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "ChatMessages"

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("ChatSessions.session_id", ondelete="CASCADE"), nullable=False)
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)   # user | bot | staff
    message_content: Mapped[str] = mapped_column(Text, nullable=False)
    intent: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence_score: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    is_product_recommendation: Mapped[bool] = mapped_column(Boolean, default=False)
    recommended_product_ids: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # JSON array
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")


# ═══════════════════════════════════════════════════════════════════════════════
# AI Conversation Log
# ═══════════════════════════════════════════════════════════════════════════════

class AIConversationLog(Base):
    __tablename__ = "AIConversationLogs"

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("ChatSessions.session_id"), nullable=False)
    account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    user_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bot_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    intent_detected: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence_score: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_escalated_to_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    session: Mapped["ChatSession"] = relationship("ChatSession")
    account: Mapped[Optional["Account"]] = relationship("Account")


# ═══════════════════════════════════════════════════════════════════════════════
# Support / FAQ
# ═══════════════════════════════════════════════════════════════════════════════

class FAQ(Base):
    __tablename__ = "FAQs"

    faq_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String(500), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())


class Notification(Base):
    __tablename__ = "Notifications"

    notification_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    account: Mapped[Optional["Account"]] = relationship("Account", back_populates="notifications")


# ═══════════════════════════════════════════════════════════════════════════════
# Inventory / Receipt
# ═══════════════════════════════════════════════════════════════════════════════

class ReceiptShipment(Base):
    __tablename__ = "ReceiptShipments"

    receipt_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("Products.product_id"), nullable=False)
    supplier_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Suppliers.supplier_id"), nullable=True)
    order_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("Orders.order_id"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # IN | OUT
    reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    product: Mapped["Product"] = relationship("Product")
    supplier: Mapped[Optional["Supplier"]] = relationship("Supplier")
    order: Mapped[Optional["Order"]] = relationship("Order")


# ═══════════════════════════════════════════════════════════════════════════════
# Knowledge Base (for AI)
# ═══════════════════════════════════════════════════════════════════════════════

class KnowledgeChunk(Base):
    __tablename__ = "KnowledgeChunks"

    chunk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    source_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    source_table: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    embedding_vector: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    chunk_metadata: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
