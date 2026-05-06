"""
ReceiptShipments Controller - Quan ly nhap/xuat kho
Tuong duong Controllers/ReceiptShipmentsController.cs trong C#
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.ReceiptShipment import ReceiptShipment
from Models.Product import Product
from Models.Supplier import Supplier
from Models.Inventory import Inventory

router = APIRouter(prefix="/ReceiptShipments")


class ReceiptShipmentCreate(BaseModel):
    product_id: int
    supplier_id: int
    order_id: Optional[int] = None
    receipt_type: str
    quantity: int
    unit_price: Optional[int] = None
    total_amount: Optional[int] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None


def _receipt_to_dict(r: ReceiptShipment) -> dict:
    return {
        "receipt_id": r.receipt_id,
        "product_id": r.product_id,
        "supplier_id": r.supplier_id,
        "order_id": r.order_id,
        "receipt_type": r.receipt_type,
        "quantity": r.quantity,
        "unit_price": r.unit_price,
        "total_amount": r.total_amount,
        "notes": r.notes,
        "receipt_date": r.receipt_date.isoformat() if r.receipt_date else None,
        "created_by": r.created_by,
    }


@router.get("")
def list_receipts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(ReceiptShipment)
    total = query.count()
    items = query.order_by(ReceiptShipment.receipt_id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [_receipt_to_dict(r) for r in items],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@router.get("/{receipt_id}")
def get_receipt(receipt_id: int, db: Session = Depends(get_db)):
    receipt = db.query(ReceiptShipment).filter(ReceiptShipment.receipt_id == receipt_id).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return _receipt_to_dict(receipt)


@router.post("")
def create_receipt(payload: ReceiptShipmentCreate, db: Session = Depends(get_db)):
    receipt_type = payload.receipt_type.strip().title()
    if receipt_type not in ["Import", "Export"]:
        raise HTTPException(status_code=400, detail="Invalid receipt_type")
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    product = db.query(Product).filter(Product.product_id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    supplier = db.query(Supplier).filter(Supplier.supplier_id == payload.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=400, detail="Supplier not found")

    inventory = db.query(Inventory).filter(Inventory.product_id == payload.product_id).first()
    if not inventory:
        inventory = Inventory(product_id=payload.product_id, quantity_in_stock=product.stock_quantity or 0)
        db.add(inventory)
        db.flush()

    if receipt_type == "Export" and inventory.quantity_in_stock < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    total_amount = payload.total_amount
    if total_amount is None and payload.unit_price is not None:
        total_amount = payload.unit_price * payload.quantity

    receipt = ReceiptShipment(
        product_id=payload.product_id,
        supplier_id=payload.supplier_id,
        order_id=payload.order_id,
        receipt_type=receipt_type,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
        total_amount=total_amount,
        notes=payload.notes,
        created_by=payload.created_by,
    )
    db.add(receipt)

    if receipt_type == "Import":
        inventory.quantity_in_stock += payload.quantity
        product.stock_quantity = (product.stock_quantity or 0) + payload.quantity
    else:
        inventory.quantity_in_stock -= payload.quantity
        product.stock_quantity = max(0, (product.stock_quantity or 0) - payload.quantity)

    db.commit()
    db.refresh(receipt)
    return _receipt_to_dict(receipt)
