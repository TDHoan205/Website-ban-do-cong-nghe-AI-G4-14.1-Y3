"""
Inventory Model - Ton kho
Tuong duong Models/Inventory.cs trong C#
"""
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, DateTime, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship
# pyrefly: ignore [missing-import]
from sqlalchemy.sql import func
from Data.database import Base


class Inventory(Base):
    __tablename__ = "Inventory"

    inventory_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.product_id"), unique=True, nullable=False)
    quantity_in_stock = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=5)
    max_stock_level = Column(Integer, default=100)
    last_restock_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    product = relationship("Product", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory(product_id={self.product_id}, qty={self.quantity_in_stock})>"
