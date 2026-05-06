"""
ReceiptShipment Model - Nhap/Xuat kho
Tuong duong Models/ReceiptShipment.cs trong C#
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class ReceiptShipment(Base):
    __tablename__ = "ReceiptShipments"

    receipt_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("Suppliers.supplier_id"), nullable=False)
    order_id = Column(Integer, ForeignKey("Orders.order_id"), nullable=True)
    receipt_type = Column(String(20), nullable=False)  # Import / Export
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer)
    total_amount = Column(Integer)
    notes = Column(String(500))
    receipt_date = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("Accounts.account_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="receipt_shipments")
    supplier = relationship("Supplier", back_populates="receipt_shipments")
    order = relationship("Order", back_populates="receipt_shipments")
    creator = relationship("Account")

    def __repr__(self):
        return f"<ReceiptShipment(type='{self.receipt_type}', qty={self.quantity})>"
