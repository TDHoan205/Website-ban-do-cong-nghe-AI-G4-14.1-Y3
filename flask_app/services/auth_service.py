"""
Authentication service – login, logout, password hashing, session management.
Uses bcrypt for secure password hashing.
"""
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from ..models import Account, Role


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    import bcrypt
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    import bcrypt
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False


class AuthService:
    """Handles all authentication operations against the real SQL Server database."""

    def __init__(self, db: Session):
        self.db = db

    # ── Account queries ──────────────────────────────────────────────

    def get_account_by_username(self, username: str) -> Optional[Account]:
        return (
            self.db.query(Account)
            .filter(Account.username == username, Account.is_active == True)
            .first()
        )

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        return self.db.query(Account).filter(Account.account_id == account_id).first()

    def get_account_by_email(self, email: str) -> Optional[Account]:
        return (
            self.db.query(Account)
            .filter(Account.email == email, Account.is_active == True)
            .first()
        )

    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.role_name == role_name).first()

    def get_all_accounts(self) -> list[Account]:
        return self.db.query(Account).all()

    # ── Authentication ──────────────────────────────────────────────

    def authenticate(self, username: str, password: str) -> Optional[Account]:
        """Verify username + password. Returns Account if valid, None otherwise."""
        account = self.get_account_by_username(username)
        if not account:
            return None
        if not account.is_active:
            return None
        if not verify_password(password, account.password_hash):
            return None
        return account

    def create_account(
        self,
        username: str,
        password: str,
        email: str,
        full_name: str,
        phone: Optional[str] = None,
        role_name: str = "Customer",
    ) -> Account:
        """Register a new account with a hashed password."""
        role = self.get_role_by_name(role_name)
        if not role:
            role = self.get_role_by_name("Customer")

        account = Account(
            username=username,
            password_hash=hash_password(password),
            email=email,
            full_name=full_name,
            phone=phone,
            role_id=role.role_id,
            is_active=True,
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_password(self, account_id: int, new_password: str) -> bool:
        """Update a user's password."""
        account = self.get_account_by_id(account_id)
        if not account:
            return False
        account.password_hash = hash_password(new_password)
        account.updated_at = datetime.now()
        self.db.commit()
        return True

    def set_reset_token(self, email: str) -> Optional[str]:
        """Generate and store a reset token for password recovery."""
        import secrets
        account = self.get_account_by_email(email)
        if not account:
            return None
        token = secrets.token_hex(32)
        account.reset_token = token
        account.reset_token_expiry = datetime.now() + timedelta(hours=1)
        account.updated_at = datetime.now()
        self.db.commit()
        return token

    def verify_reset_token(self, token: str) -> Optional[Account]:
        """Verify a password-reset token and return the account."""
        account = (
            self.db.query(Account)
            .filter(
                Account.reset_token == token,
                Account.reset_token_expiry > datetime.now(),
            )
            .first()
        )
        return account
