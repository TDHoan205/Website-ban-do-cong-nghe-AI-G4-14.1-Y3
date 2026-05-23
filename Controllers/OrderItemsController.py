"""
OrderItems Controller - Quan ly item don hang
Tuong duong Controllers/OrderItemsController.cs trong C#
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.Order import OrderItem

router = APIRouter(prefix="/OrderItems")


@router.get("")
def list_order_items(order_id: int = Query(..., ge=1), db: Session = Depends(get_db)):
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return [
        {
            "order_item_id": i.order_item_id,
            "order_id": i.order_id,
            "product_id": i.product_id,
            "variant_id": i.variant_id,
            "product_name": i.product_name,
            "variant_name": i.variant_name,
            "quantity": i.quantity,
            "unit_price": float(i.unit_price),
            "subtotal": float(i.subtotal),
        }
        for i in items
    ]
