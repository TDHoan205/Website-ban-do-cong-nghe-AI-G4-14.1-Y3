"""
Auth Service - Xac thuc nguoi dung
Tuong duong Services/AuthService.cs trong ASP.NET Core
"""
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from Models.Account import Account, Role
import uuid

# Cau hinh JWT
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        return pwd_context.hash(safe)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Xac minh password"""
        if not hashed_password:
            return False
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return plain_password == hashed_password

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
            raise ValueError("Email da ton tai")

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
