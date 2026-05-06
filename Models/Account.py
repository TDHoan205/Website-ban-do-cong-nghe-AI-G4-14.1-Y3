"""
Account Model - Tài khoản người dùng
Tương đương Models/Account.cs trong C#
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class Account(Base):
    __tablename__ = "Accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    full_name = Column(String(100))
    phone = Column(String(20))
    address = Column(String(255))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("Roles.role_id"), nullable=False)
    reset_token = Column(String(64))
    reset_token_expiry = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    role = relationship("Role", back_populates="accounts")
    employee = relationship("Employee", back_populates="account", uselist=False)
    orders = relationship("Order", back_populates="account")
    carts = relationship("Cart", back_populates="account")

    @property
    def role_name(self) -> str:
        return self.role.role_name if self.role else "Customer"

    def __repr__(self):
        return f"<Account(username='{self.username}', role='{self.role_name}')>"


"""
Employee Model - Nhân viên
"""


class Employee(Base):
    __tablename__ = "Employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("Accounts.account_id"), unique=True, nullable=False)
    department = Column(String(50))
    position = Column(String(50))
    hire_date = Column(DateTime(timezone=True))
    salary = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="employee")

    def __repr__(self):
        return f"<Employee(account_id={self.account_id}, dept='{self.department}')>"


"""
Role Model - Vai trò người dùng
"""


class Role(Base):
    __tablename__ = "Roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    permissions = Column(String(1000))  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    accounts = relationship("Account", back_populates="role")

    def __repr__(self):
        return f"<Role(role_name='{self.role_name}')>"
