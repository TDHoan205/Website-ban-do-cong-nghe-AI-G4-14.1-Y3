"""
User Model - Tài khoản người dùng
Tương đương Models/Account.cs trong ASP.NET Core
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    phone = Column(String(20))
    address = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="Customer")  # Customer, Admin, Employee
    avatar_url = Column(String(500))
    reset_token = Column(String(64))
    reset_token_expiry = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    cart = relationship("Cart", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"
