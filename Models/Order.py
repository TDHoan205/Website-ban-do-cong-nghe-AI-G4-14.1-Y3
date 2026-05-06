"""
Order Model - Đơn hàng
Tương đương Models/Order.cs trong C#
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class Order(Base):
    __tablename__ = "Orders"

    order_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), default="Pending")  # Pending, Confirmed, Processing, Shipped, Delivered, Cancelled
    customer_name = Column(String(100))
    customer_phone = Column(String(20))
    customer_address = Column(String(255))
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    account = relationship("Account", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    receipt_shipments = relationship("ReceiptShipment", back_populates="order")

    def __repr__(self):
        return f"<Order(order_id={self.order_id}, status='{self.status}')>"


"""
OrderItem Model - Item trong đơn hàng
Tương đương Models/OrderItem.cs trong C#
"""


class OrderItem(Base):
    __tablename__ = "OrderItems"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False)
    variant_id = Column(Integer, ForeignKey("ProductVariants.variant_id"), nullable=True)
    product_name = Column(String(255), nullable=False)  # Lưu tên tại thời điểm đặt
    variant_name = Column(String(100))  # Lưu tên variant tại thời điểm đặt
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    variant = relationship("ProductVariant", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(product='{self.product_name}', qty={self.quantity})>"


"""
OrderStatus Model - Trạng thái đơn hàng
Tương đương Models/OrderStatus.cs trong C#
"""


class OrderStatus:
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

    STATUSES = [
        (PENDING, "Chờ xác nhận"),
        (CONFIRMED, "Đã xác nhận"),
        (PROCESSING, "Đang xử lý"),
        (SHIPPED, "Đã gửi hàng"),
        (DELIVERED, "Đã giao hàng"),
        (CANCELLED, "Đã hủy"),
    ]

    @classmethod
    def get_display(cls, status: str) -> str:
        for key, display in cls.STATUSES:
            if key == status:
                return display
        return status
