"""
Payment Service - Xử lý thanh toán QR Banking
"""
import re
import uuid
import datetime
import base64
import io
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc

from Models.Payment import Payment, PaymentStatus
from Models.Cart import CartItem
from Models.Product import Product, ProductVariant


# ============ Cấu hình ngân hàng ============
BANK_CONFIG = {
    "bank_code": "MB",
    "bank_name": "MB Bank",
    "bank_account": "0386267692",
    "bank_account_name": "TRAN ANH QUAN",
    "bank_bin": "970422",  # BIN của MB Bank
}

# VietQR format template (định dạng chuẩn Quick Link của VietQR)
QR_TEMPLATE = (
    "https://img.vietqr.io/image/{bank_code}-{account}-compact2.png"
    "?amount={amount}&addInfo={message}&accountName={account_name}"
)


class PaymentService:
    PAYMENT_EXPIRY_MINUTES = 30

    def __init__(self, db: Session):
        self.db = db

    # ============ Tạo mã đơn hàng ============
    def _generate_order_id(self) -> str:
        """Tạo mã đơn hàng unique: DH + timestamp + random"""
        ts = datetime.datetime.now().strftime("%m%d%H%M%S")
        rnd = uuid.uuid4().hex[:4].upper()
        return f"DH{ts}{rnd}"

    # ============ Tạo nội dung chuyển khoản ============
    def _generate_transfer_content(self, order_id: str) -> str:
        """Nội dung = mã đơn hàng"""
        return order_id

    # ============ Tạo QR string ============
    def _build_qr_string(self, amount: int, message: str) -> str:
        """Build VietQR format string"""
        account = BANK_CONFIG["bank_account"]
        return f"{BANK_CONFIG['bank_bin']}{account}{amount}{message}"

    # ============ Tạo QR image URL ============
    def _build_qr_url(self, amount: int, message: str) -> str:
        """Build VietQR image URL"""
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        encoded_account_name = urllib.parse.quote(BANK_CONFIG["bank_account_name"].upper())
        return QR_TEMPLATE.format(
            bank_code=BANK_CONFIG["bank_code"].lower(),
            account=BANK_CONFIG["bank_account"],
            amount=amount,
            message=encoded_message,
            account_name=encoded_account_name,
        )

    # ============ Tạo payment record ============
    def create_payment(
        self,
        account_id: int,
        amount: int,
    ) -> Payment:
        """Tạo bản ghi thanh toán mới"""

        # Kiểm tra payment đang pending cho account này
        existing = self.db.query(Payment).filter(
            Payment.account_id == account_id,
            Payment.status == PaymentStatus.PENDING
        ).first()

        if existing:
            # Nếu chưa hết hạn, dùng lại
            expires_at_naive = existing.expires_at.replace(tzinfo=None) if existing.expires_at else None
            if expires_at_naive and expires_at_naive > datetime.datetime.now():
                return existing
            # Hết hạn thì mark expired
            existing.status = PaymentStatus.EXPIRED
            self.db.commit()

        order_id = self._generate_order_id()
        transfer_content = self._generate_transfer_content(order_id)
        qr_url = self._build_qr_url(amount, transfer_content)
        qr_string = self._build_qr_string(amount, transfer_content)

        expires_at = datetime.datetime.now() + datetime.timedelta(
            minutes=self.PAYMENT_EXPIRY_MINUTES
        )

        payment = Payment(
            order_id=order_id,
            account_id=account_id,
            amount=amount,
            payment_method="QR_BANKING",
            transfer_content=transfer_content,
            qr_data=qr_string,
            qr_image_base64=qr_url,
            bank_code=BANK_CONFIG["bank_code"],
            bank_account=BANK_CONFIG["bank_account"],
            bank_account_name=BANK_CONFIG["bank_account_name"],
            status=PaymentStatus.PENDING,
            expires_at=expires_at,
        )

        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    # ============ Lấy payment ============
    def get_payment_by_order_id(self, order_id: str) -> Optional[Payment]:
        return self.db.query(Payment).filter(
            Payment.order_id == order_id
        ).first()

    def get_payment_by_account_pending(self, account_id: int) -> Optional[Payment]:
        return self.db.query(Payment).filter(
            Payment.account_id == account_id,
            Payment.status == PaymentStatus.PENDING
        ).order_by(desc(Payment.created_at)).first()

    # ============ Xác nhận thanh toán (manual verify) ============
    def verify_payment(
        self,
        order_id: str,
        transaction_code: Optional[str] = None,
        verified_by: str = "manual"
    ) -> Tuple[bool, str]:
        """Xác nhận thanh toán - backend verify"""

        payment = self.get_payment_by_order_id(order_id)
        if not payment:
            return False, "Không tìm thấy thanh toán"

        if payment.status == PaymentStatus.PAID:
            return True, "Đã thanh toán rồi"

        if payment.status == PaymentStatus.EXPIRED:
            return False, "Mã thanh toán đã hết hạn"

        expires_at_naive = payment.expires_at.replace(tzinfo=None) if payment.expires_at else None
        if expires_at_naive and expires_at_naive < datetime.datetime.now():
            payment.status = PaymentStatus.EXPIRED
            self.db.commit()
            return False, "Mã thanh toán đã hết hạn"

        # Cập nhật paid
        payment.status = PaymentStatus.PAID
        payment.paid_at = datetime.datetime.now()
        payment.verified_by = verified_by
        if transaction_code:
            payment.transaction_code = transaction_code

        self.db.commit()
        return True, "Xác nhận thanh toán thành công"

    # ============ Mark expired ============
    def mark_expired(self, payment: Payment) -> None:
        if payment.status == PaymentStatus.PENDING:
            payment.status = PaymentStatus.EXPIRED
            self.db.commit()

    # ============ Get payment info for display ============
    def get_payment_display_info(self, order_id: str) -> Optional[dict]:
        """Trả về thông tin hiển thị QR"""
        payment = self.get_payment_by_order_id(order_id)
        if not payment:
            return None

        remaining = None
        if payment.expires_at:
            expires_at_naive = payment.expires_at.replace(tzinfo=None)
            delta = expires_at_naive - datetime.datetime.now()
            remaining = max(0, int(delta.total_seconds()))

        return {
            "order_id": payment.order_id,
            "amount": payment.amount,
            "transfer_content": payment.transfer_content,
            "qr_image_url": payment.qr_image_base64,
            "bank_code": payment.bank_code,
            "bank_name": BANK_CONFIG["bank_name"],
            "bank_account": payment.bank_account,
            "bank_account_name": payment.bank_account_name,
            "status": payment.status,
            "remaining_seconds": remaining,
            "created_at": payment.created_at.isoformat() if payment.created_at else None,
            "expires_at": payment.expires_at.isoformat() if payment.expires_at else None,
        }
