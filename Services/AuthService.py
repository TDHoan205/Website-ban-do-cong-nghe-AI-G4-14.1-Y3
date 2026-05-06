"""
Auth Service - Xác thực người dùng
Tương đương Services/AuthService.cs trong ASP.NET Core
"""
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from Models.Account import Account, Role
import uuid

# Cấu hình JWT
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        """Mã hóa password"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Xác minh password"""
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, account_id: int, username: str, role: str) -> str:
        """Tạo JWT token"""
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(account_id),
            "username": username,
            "role": role,
            "exp": expire
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode_token(self, token: str) -> Optional[dict]:
        """Giải mã JWT token"""
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
        """Lấy account theo username"""
        return self.db.query(Account).filter(Account.username == username).first()

    def get_account_by_email(self, email: str) -> Optional[Account]:
        """Lấy account theo email"""
        return self.db.query(Account).filter(Account.email == email).first()

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """Lấy account theo ID"""
        return self.db.query(Account).filter(Account.account_id == account_id).first()

    def authenticate_user(self, username: str, password: str) -> Optional[Account]:
        """Xác thực đăng nhập"""
        account = self.get_account_by_username(username)
        if not account:
            return None
        if not self.verify_password(password, account.password_hash):
            return None
        if not account.is_active:
            return None
        return account

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: str = None,
        phone: str = None
    ) -> Account:
        """Đăng ký account mới"""
        # Kiểm tra trùng lặp
        if self.get_account_by_username(username):
            raise ValueError("Username đã tồn tại")
        if self.get_account_by_email(email):
            raise ValueError("Email đã tồn tại")

        customer_role = self.db.query(Role).filter(Role.role_name == "Customer").first()
        if not customer_role:
            customer_role = Role(role_name="Customer", description="Default customer role")
            self.db.add(customer_role)
            self.db.commit()
            self.db.refresh(customer_role)

        account = Account(
            username=username,
            email=email,
            password_hash=self.hash_password(password),
            full_name=full_name,
            phone=phone,
            role_id=customer_role.role_id,
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
