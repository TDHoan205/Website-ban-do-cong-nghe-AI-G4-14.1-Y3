"""
Auth helpers
"""
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from Services.AuthService import AuthService


def require_account(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Login required")
    auth_service = AuthService(db)
    account = auth_service.get_current_account_from_token(token)
    if not account:
        raise HTTPException(status_code=401, detail="Login required")
    return account
