"""
Payment Model - Thanh toán QR
"""
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Data.database import Base


class PaymentStatus:
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"

    @classmethod
    def all(cls):
        return [cls.PENDING, cls.PAID, cls.FAILED, cls.EXPIRED]


class Payment(Base):
    __tablename__ = "Payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(50), unique=True, nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("Accounts.account_id"), nullable=True)
    amount = Column(BigInteger, nullable=False)  # Số tiền VND
    payment_method = Column(String(20), default="QR_BANKING")
    transaction_code = Column(String(100), nullable=True)  # Mã giao dịch ngân hàng
    transfer_content = Column(String(200), nullable=True)  # Nội dung chuyển khoản (DHxxxxx)
    status = Column(String(20), default=PaymentStatus.PENDING)
    qr_data = Column(Text, nullable=True)  # Raw QR string ( VietQR format)
    qr_image_base64 = Column(Text, nullable=True)  # QR image as base64
    bank_code = Column(String(20), nullable=True)  # MB, VCB, TCB...
    bank_account = Column(String(50), nullable=True)
    bank_account_name = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    verified_by = Column(String(50), nullable=True)  # 'manual' or 'auto'
    notes = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<Payment(order_id={self.order_id}, status={self.status}, amount={self.amount})>"
