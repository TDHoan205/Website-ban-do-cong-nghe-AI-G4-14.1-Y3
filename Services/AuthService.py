"""
Auth Service - Xac thuc nguoi dung
Tuong duong Services/AuthService.cs trong ASP.NET Core
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func as sql_func
import bcrypt
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from Models.Account import Account, Role
from Models.Order import Order
from Models.Wishlist import Wishlist
import uuid

# Cau hinh JWT
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def _safe_password(password: str) -> str:
    """Cat password thanh 72 bytes de tranh loi bcrypt"""
    encoded = password.encode("utf-8")
    if len(encoded) <= 72:
        return password
    return encoded[:72].decode("utf-8", errors="ignore")


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        """Ma hoa password"""
        safe = _safe_password(password)
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(safe.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Xac minh password"""
        if not hashed_password:
            return False
            
        # Fallback cho data seed
        if not hashed_password.startswith("$2"):
            return plain_password == hashed_password
            
        try:
            safe = _safe_password(plain_password)
            return bcrypt.checkpw(safe.encode("utf-8"), hashed_password.encode("utf-8"))
        except Exception:
            return False

    def create_access_token(self, account_id: int, username: str, role: str) -> str:
        """Tao JWT token"""
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(account_id),
            "username": username,
            "role": role,
            "exp": expire
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> Optional[dict]:
        """Giai ma JWT token"""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            return None

    def get_current_account_from_token(self, token: str) -> Optional[Account]:
        """Lay account tu token"""
        payload = self.decode_token(token)
        if not payload or "sub" not in payload:
            return None
        try:
            account_id = int(payload["sub"])
        except ValueError:
            return None
        return self.get_account_by_id(account_id)

    def get_account_by_username(self, username: str) -> Optional[Account]:
        """Lay account theo username"""
        return self.db.query(Account).options(joinedload(Account.role)).filter(Account.username == username).first()

    def get_account_by_email(self, email: str) -> Optional[Account]:
        """Lay account theo email"""
        return self.db.query(Account).options(joinedload(Account.role)).filter(Account.email == email).first()

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """Lay account theo ID"""
        return self.db.query(Account).options(joinedload(Account.role)).filter(Account.account_id == account_id).first()

    def authenticate_user(self, username: str, password: str) -> Optional[Account]:
        """Xac thuc dang nhap"""
        account = self.get_account_by_username(username)
        if not account:
            return None

        pwd_hash = account.password_hash or ""

        if not account.is_active:
            return None

        if self.verify_password(password, pwd_hash):
            return account

        return None

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = None,
        phone: str = None,
        address: str = None,
        role_name: str = "Customer"
    ) -> Account:
        """Dang ky account moi voi role tuy chon"""
        if self.get_account_by_username(username):
            raise ValueError("Username da ton tai")
        if self.get_account_by_email(email):
            raise ValueError('Email đã tồn tại')

        # Tim role theo ten, chi cho phep Customer hoac Admin
        safe_role = "Customer" if role_name not in ("Customer", "Admin") else role_name
        role = self.db.query(Role).filter(Role.role_name == safe_role).first()
        if not role:
            role = Role(role_name=safe_role)
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)

        account = Account(
            username=username,
            email=email,
            password_hash=self.hash_password(password),
            full_name=full_name,
            phone=phone,
            address=address,
            role_id=role.role_id,
            is_active=True
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def create_reset_token(self, email: str) -> str:
        """Tao token reset mat khau"""
        account = self.get_account_by_email(email)
        if not account:
            raise ValueError("Email not found")
        token = uuid.uuid4().hex
        account.reset_token = token
        account.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)
        self.db.commit()
        return token

    def reset_password(self, token: str, new_password: str) -> bool:
        """Reset mat khau theo token"""
        if not token:
            return False
        account = self.db.query(Account).filter(Account.reset_token == token).first()
        if not account or not account.reset_token_expiry:
            return False
        if account.reset_token_expiry < datetime.utcnow():
            return False
        account.password_hash = self.hash_password(new_password)
        account.reset_token = None
        account.reset_token_expiry = None
        self.db.commit()
        return True

    def update_password(self, account_id: int, current_password: str, new_password: str) -> tuple[bool, str]:
        """
        Cap nhat mat khau moi cho tai khoan.
        Tra ve (True, "") neu thanh cong.
        Tra ve (False, message) neu that bai.
        """
        account = self.get_account_by_id(account_id)
        if not account:
            return False, "Tài khoản không tồn tại."

        if not account.is_active:
            return False, "Tài khoản đã bị khóa."

        pwd_hash = account.password_hash or ""
        if not self.verify_password(current_password, pwd_hash):
            return False, "Mật khẩu hiện tại không chính xác."

        if self.verify_password(new_password, pwd_hash):
            return False, "Mật khẩu mới không được trùng với mật khẩu hiện tại."

        account.password_hash = self.hash_password(new_password)
        account.updated_at = datetime.utcnow()
        self.db.commit()
        return True, ""

    def get_user_statistics(self, account_id: int) -> dict:
        """
        Lay thong ke tai khoan nguoi dung.
        Chi tinh don hang da giao thanh cong (Delivered).
        """

        # Dem so don hang da giao thanh cong
        delivered_count = self.db.query(sql_func.count(Order.order_id)).filter(
            Order.account_id == account_id,
            Order.status == "Delivered"
        ).scalar() or 0

        # Tong chi tieu tu don hang da giao thanh cong
        total = self.db.query(sql_func.sum(Order.total_amount)).filter(
            Order.account_id == account_id,
            Order.status == "Delivered"
        ).scalar() or 0

        # Convert Decimal to int/float
        if hasattr(total, '__float__'):
            total_spent = int(total)
        elif total is None:
            total_spent = 0
        else:
            try:
                total_spent = int(total)
            except (ValueError, TypeError):
                total_spent = 0

        # Dem so san pham yeu thich
        wishlist_count = self.db.query(sql_func.count(Wishlist.wishlist_id)).filter(
            Wishlist.account_id == account_id
        ).scalar() or 0

        return {
            "total_orders": delivered_count,
            "total_spent": total_spent,
            "wishlist_count": wishlist_count,
        }

    def seed_roles(self):
        """Tao 2 role mac dinh neu chua ton tai"""
        existing = self.db.query(Role).all()
        if existing:
            return

        role_admin = Role(role_name="Admin")
        role_customer = Role(role_name="Customer")
        self.db.add(role_admin)
        self.db.add(role_customer)
        self.db.commit()
