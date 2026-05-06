"""
Category Model - Danh mục sản phẩm
Tương đương Models/Category.cs trong C#
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class Category(Base):
    __tablename__ = "Categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    image_url = Column(String(500))
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"
