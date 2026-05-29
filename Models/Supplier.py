"""
Supplier Model - Nhà cung cấp
Tương đương Models/Supplier.cs trong C#
"""
from sqlalchemy import Column, Integer, String, Unicode, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class Supplier(Base):
    __tablename__ = "Suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(255), nullable=False)
    contact_person = Column(Unicode(100))
    phone = Column(Unicode(20))
    email = Column(Unicode(100))
    address = Column(Unicode(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship("Product", back_populates="supplier")
    receipt_shipments = relationship("ReceiptShipment", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(name='{self.name}')>"
