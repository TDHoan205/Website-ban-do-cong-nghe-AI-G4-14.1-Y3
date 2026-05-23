"""
Inventory Controller - Quan ly ton kho
Tuong duong Controllers/InventoryController.cs trong C#
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.Inventory import Inventory

router = APIRouter(prefix="/Inventory")


class InventoryUpdate(BaseModel):
    quantity_in_stock: Optional[int] = None
    min_stock_level: Optional[int] = None
    max_stock_level: Optional[int] = None


def _inventory_to_dict(i: Inventory) -> dict:
    return {
        "inventory_id": i.inventory_id,
        "product_id": i.product_id,
        "quantity_in_stock": i.quantity_in_stock,
        "min_stock_level": i.min_stock_level,
        "max_stock_level": i.max_stock_level,
        "last_restock_date": i.last_restock_date.isoformat() if i.last_restock_date else None,
    }


@router.get("")
def list_inventory(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Inventory)
    total = query.count()
    items = query.order_by(Inventory.inventory_id).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [_inventory_to_dict(i) for i in items],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@router.put("/{inventory_id}")
def update_inventory(inventory_id: int, payload: InventoryUpdate, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(inventory, key, value)
    db.commit()
    db.refresh(inventory)
    return _inventory_to_dict(inventory)
