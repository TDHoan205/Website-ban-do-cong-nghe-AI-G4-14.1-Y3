"""
Accounts Controller - Quan ly tai khoan
Tuong duong Controllers/AccountsController.cs trong C#
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.Account import Account, Role
from Services.AccountService import AccountService

router = APIRouter(prefix="/Accounts")


def _require_admin(db: Session, actor_account_id: Optional[int]) -> None:
    if actor_account_id is None:
        raise HTTPException(status_code=401, detail="Actor account is required")
    actor = db.query(Account).filter(Account.account_id == actor_account_id).first()
    if not actor or not actor.role or actor.role.role_name != "Admin":
        raise HTTPException(status_code=403, detail="Admin permission required")


def _account_to_dict(account: Account) -> dict:
    return {
        "account_id": account.account_id,
        "username": account.username,
        "email": account.email,
        "full_name": account.full_name,
        "phone": account.phone,
        "address": account.address,
        "is_active": account.is_active,
        "role_id": account.role_id,
        "role_name": account.role.role_name if account.role else None,
        "created_at": account.created_at.isoformat() if account.created_at else None,
    }


class AccountCreate(BaseModel):
    username: str
    password: str
    email: str
    role_id: int
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class AccountUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None


@router.get("")
def list_accounts(
    search: Optional[str] = Query(None),
    sort_order: str = Query("username"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = AccountService(db)
    paged = service.get_all_accounts(search=search, sort_order=sort_order, page_number=page, page_size=page_size)
    return {
        "items": [_account_to_dict(a) for a in paged],
        "page": paged.current_page,
        "page_size": paged.page_size,
        "total": paged.total_count,
        "total_pages": paged.total_pages,
    }


@router.get("/Roles")
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).order_by(Role.role_name).all()
    return [
        {
            "role_id": r.role_id,
            "role_name": r.role_name,
            "description": r.description,
        }
        for r in roles
    ]


@router.get("/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.account_id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return _account_to_dict(account)


@router.post("")
def create_account(
    payload: AccountCreate,
    actor_account_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    # Basic validation
    username = payload.username.strip()
    email = payload.email.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    _require_admin(db, actor_account_id)
    service = AccountService(db)
    if db.query(Account).filter(Account.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(Account).filter(Account.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    if payload.phone:
        if db.query(Account).filter(Account.phone == payload.phone).first():
            raise HTTPException(status_code=400, detail="Phone already exists")
    role = db.query(Role).filter(Role.role_id == payload.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")
    account = service.create_account(
        username=username,
        password=payload.password,
        email=email,
        role_id=payload.role_id,
        full_name=payload.full_name,
        phone=payload.phone,
        address=payload.address,
    )
    return _account_to_dict(account)


@router.put("/{account_id}")
def update_account(
    account_id: int,
    payload: AccountUpdate,
    actor_account_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    _require_admin(db, actor_account_id)
    service = AccountService(db)
    if payload.email:
        payload.email = payload.email.strip()
        exists = db.query(Account).filter(
            Account.email == payload.email,
            Account.account_id != account_id
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already exists")
    if payload.phone:
        exists = db.query(Account).filter(
            Account.phone == payload.phone,
            Account.account_id != account_id
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail="Phone already exists")
    if payload.role_id is not None:
        role = db.query(Role).filter(Role.role_id == payload.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Role not found")
    account = service.update_account(
        account_id=account_id,
        email=payload.email,
        full_name=payload.full_name,
        phone=payload.phone,
        address=payload.address,
        role_id=payload.role_id,
        is_active=payload.is_active,
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return _account_to_dict(account)


@router.delete("/{account_id}")
def delete_account(account_id: int, actor_account_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    _require_admin(db, actor_account_id)
    service = AccountService(db)
    ok = service.delete_account(account_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"success": True}
