"""
Account Service - Xác thực và quản lý tài khoản
Tương đương Services/AccountService.cs trong C#
"""
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import Optional, List
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from Models.Account import Account, Role
from Utilities import PagedList

# JWT Configuration
SECRET_KEY = "your-super-secret-key-change-in-production-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AccountService:
    def __init__(self, db: Session):
        self.db = db

    # ============ Password Hashing ============
    def hash_password(self, password: str) -> str:
        """Mã hóa password"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Xác minh password"""
        return pwd_context.verify(plain_password, hashed_password)

    # ============ JWT Token ============
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

    def get_current_account(self, token: str) -> Optional[Account]:
        """Lấy account từ token"""
        payload = self.decode_token(token)
        if not payload:
            return None
        return self.get_account_by_id(int(payload["sub"]))

    # ============ Account CRUD ============
    def get_all_accounts(
        self,
        search: Optional[str] = None,
        sort_order: str = "username",
        page_number: int = 1,
        page_size: int = 10
    ) -> PagedList:
        """Lấy danh sách tài khoản có phân trang"""

        query = self.db.query(Account).join(Role)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Account.username.ilike(search_term),
                    Account.full_name.ilike(search_term),
                    Account.email.ilike(search_term)
                )
            )

        # Sort
        if sort_order == "username":
            query = query.order_by(Account.username)
        elif sort_order == "username_desc":
            query = query.order_by(desc(Account.username))
        elif sort_order == "fullname":
            query = query.order_by(Account.full_name)
        elif sort_order == "fullname_desc":
            query = query.order_by(desc(Account.full_name))
        elif sort_order == "email":
            query = query.order_by(Account.email)
        elif sort_order == "email_desc":
            query = query.order_by(desc(Account.email))
        elif sort_order == "role":
            query = query.order_by(Role.role_name)
        elif sort_order == "role_desc":
            query = query.order_by(desc(Role.role_name))
        else:
            query = query.order_by(Account.username)

        return PagedList.create(query, page_number, page_size)

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        """Lấy tài khoản theo ID"""
        return self.db.query(Account).filter(Account.account_id == account_id).first()

    def get_account_by_username(self, username: str) -> Optional[Account]:
        """Lấy tài khoản theo username"""
        return self.db.query(Account).filter(Account.username == username).first()

    def get_account_by_email(self, email: str) -> Optional[Account]:
        """Lấy tài khoản theo email"""
        return self.db.query(Account).filter(Account.email == email).first()

    def create_account(
        self,
        username: str,
        password: str,
        email: str,
        role_id: int,
        full_name: str = None,
        phone: str = None,
        address: str = None
    ) -> Account:
        """Tạo tài khoản mới"""
        # Check duplicate
        if self.get_account_by_username(username):
            raise ValueError("Tên đăng nhập đã tồn tại")

        account = Account(
            username=username,
            password_hash=self.hash_password(password),
            email=email,
            role_id=role_id,
            full_name=full_name,
            phone=phone,
            address=address,
            is_active=True
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_account(
        self,
        account_id: int,
        email: str = None,
        full_name: str = None,
        phone: str = None,
        address: str = None,
        role_id: int = None,
        is_active: bool = None
    ) -> Optional[Account]:
        """Cập nhật tài khoản"""
        account = self.get_account_by_id(account_id)
        if not account:
            return None

        if email is not None:
            account.email = email
        if full_name is not None:
            account.full_name = full_name
        if phone is not None:
            account.phone = phone
        if address is not None:
            account.address = address
        if role_id is not None:
            account.role_id = role_id
        if is_active is not None:
            account.is_active = is_active

        self.db.commit()
        self.db.refresh(account)
        return account

    def delete_account(self, account_id: int) -> bool:
        """Xóa tài khoản"""
        account = self.get_account_by_id(account_id)
        if not account:
            return False
        self.db.delete(account)
        self.db.commit()
        return True

    # ============ Authentication ============
    def authenticate(self, username: str, password: str) -> Optional[Account]:
        """Xác thực đăng nhập"""
        account = self.get_account_by_username(username)
        if not account:
            return None
        if not self.verify_password(password, account.password_hash):
            return None
        if not account.is_active:
            return None
        return account

    def register(
        self,
        username: str,
        password: str,
        email: str,
        full_name: str = None,
        phone: str = None
    ) -> Account:
        """Đăng ký tài khoản mới"""
        # Get default customer role
        customer_role = self.db.query(Role).filter(Role.role_name == "Customer").first()
        if not customer_role:
            raise ValueError("Không tìm thấy vai trò Customer")

        return self.create_account(
            username=username,
            password=password,
            email=email,
            role_id=customer_role.role_id,
            full_name=full_name,
            phone=phone
        )

    # ============ Role ============
    def get_all_roles(self) -> List[Role]:
        """Lấy danh sách vai trò"""
        return self.db.query(Role).order_by(Role.role_name).all()

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """Lấy vai trò theo ID"""
        return self.db.query(Role).filter(Role.role_id == role_id).first()
