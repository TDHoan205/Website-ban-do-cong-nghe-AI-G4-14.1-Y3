"""
Auth helpers
"""
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from Services.AuthService import AuthService


def require_account(request: Request, db: Session):
    """Bat buoc dang nhap - tra ve Account"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Login required")
    auth_service = AuthService(db)
    account = auth_service.get_current_account_from_token(token)
    if not account:
        raise HTTPException(status_code=401, detail="Login required")
    return account


def require_role(request: Request, db: Session, allowed_roles: list):
    """Bat buoc dang nhap va co role duoc phep - tra ve Account"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Login required")
    auth_service = AuthService(db)
    account = auth_service.get_current_account_from_token(token)
    if not account:
        raise HTTPException(status_code=401, detail="Login required")
    if account.role_name not in allowed_roles:
        raise HTTPException(status_code=403, detail="Forbidden: You don't have permission")
    return account


def get_current_user(request: Request, db: Session):
    """Lay thong tin user hien tai (khong raise loi) - tra ve Account hoac None"""
    token = request.cookies.get("access_token")
    if not token:
        return None
    auth_service = AuthService(db)
    return auth_service.get_current_account_from_token(token)
