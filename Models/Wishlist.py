"""
Wishlist Model - Danh sách yêu thích
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class Wishlist(Base):
    __tablename__ = "Wishlists"

    wishlist_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("Accounts.account_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Products.product_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    account = relationship("Account")
    product = relationship("Product")

    def __repr__(self):
        return f"<Wishlist(account_id={self.account_id}, product_id={self.product_id})>"
