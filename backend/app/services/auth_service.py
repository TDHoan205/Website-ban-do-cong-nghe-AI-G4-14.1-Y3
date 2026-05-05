from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.core.security import get_password_hash, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.user_id == user_id).first()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return get_password_hash(password)

    def create_user(self, username: str, email: str, password: str, **kwargs) -> User:
        hashed_password = self.hash_password(password)
        role = self.db.query(Role).filter(Role.role_name == "Customer").first()
        if not role:
            role = Role(role_name="Customer")
            self.db.add(role)
            self.db.commit()
            self.db.refresh(role)

        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role_id=role.role_id,
            **kwargs
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_password(self, user: User, new_password: str) -> bool:
        user.password_hash = self.hash_password(new_password)
        self.db.commit()
        return True

    def set_reset_token(self, user: User, token: str):
        from datetime import datetime, timedelta
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=24)
        self.db.commit()

    def verify_reset_token(self, token: str) -> User | None:
        return self.db.query(User).filter(User.reset_token == token).first()
