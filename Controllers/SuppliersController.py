"""
Suppliers Controller - Quan ly nha cung cap
Tuong duong Controllers/SuppliersController.cs trong C#
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.Supplier import Supplier

router = APIRouter(prefix="/Suppliers")


class SupplierCreate(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = True


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


def _supplier_to_dict(s: Supplier) -> dict:
    return {
        "supplier_id": s.supplier_id,
        "name": s.name,
        "contact_person": s.contact_person,
        "phone": s.phone,
        "email": s.email,
        "address": s.address,
        "is_active": s.is_active,
    }


@router.get("")
def list_suppliers(
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Supplier)
    if search:
        query = query.filter(Supplier.name.ilike(f"%{search}%"))
    total = query.count()
    items = query.order_by(Supplier.name).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [_supplier_to_dict(s) for s in items],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@router.get("/{supplier_id}")
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return _supplier_to_dict(supplier)


@router.post("")
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return _supplier_to_dict(supplier)


@router.put("/{supplier_id}")
def update_supplier(supplier_id: int, payload: SupplierUpdate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return _supplier_to_dict(supplier)


@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()
    return {"success": True}
