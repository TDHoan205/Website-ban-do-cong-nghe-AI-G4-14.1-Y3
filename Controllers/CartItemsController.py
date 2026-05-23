"""
CartItems Controller - Quan ly item gio hang
Tuong duong Controllers/CartItemsController.cs trong C#
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.Cart import Cart, CartItem

router = APIRouter(prefix="/CartItems")


@router.get("")
def list_cart_items(account_id: int = Query(..., ge=1), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.account_id == account_id).first()
    if not cart:
        return []
    items = db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).all()
    return [
        {
            "cart_item_id": i.cart_item_id,
            "cart_id": i.cart_id,
            "product_id": i.product_id,
            "variant_id": i.variant_id,
            "quantity": i.quantity,
        }
        for i in items
    ]
