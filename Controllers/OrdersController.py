"""
Orders Controller - Quan ly don hang
Tuong duong Controllers/OrdersController.cs trong C#
"""
from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.Order import Order, OrderItem, OrderStatus
from Models.Cart import Cart
from Services.OrderService import OrderService
from Utilities.auth import require_account

router = APIRouter(prefix="/Orders")

# Templates se duoc gan tu app.py
templates = None

def set_templates(t):
    global templates
    templates = t


def _get_cart_count(request: Request, db: Session) -> int:
    try:
        account = require_account(request, db)
        cart = db.query(Cart).filter(Cart.account_id == account.account_id).first()
        if cart and cart.cart_items:
            return sum(ci.quantity for ci in cart.cart_items)
    except Exception:
        pass
    return 0


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    """Trang danh sach don hang cua nguoi dung"""
    try:
        account = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)

    service = OrderService(db)
    orders = service.get_orders_by_account(account.account_id)
    cart_count = _get_cart_count(request, db)
    order_stats = service.get_order_stats_for_account(account.account_id)

    return templates.TemplateResponse(
        "Orders/index.html",
        {
            "request": request,
            "page_title": "Đơn hàng của tôi",
            "orders": orders,
            "order_stats": order_stats,
            "current_user": account,
            "cart_count": cart_count,
        }
    )




class OrderStatusUpdate(BaseModel):
    status: str


class OrderCreateFromCart(BaseModel):
    account_id: int
    customer_name: str
    customer_phone: str
    customer_address: str
    notes: Optional[str] = None


def _order_to_dict(o: Order) -> dict:
    return {
        "order_id": o.order_id,
        "account_id": o.account_id,
        "order_date": o.order_date.isoformat() if o.order_date else None,
        "total_amount": float(o.total_amount) if o.total_amount is not None else 0,
        "status": o.status,
        "customer_name": o.customer_name,
        "customer_phone": o.customer_phone,
        "customer_address": o.customer_address,
        "notes": o.notes,
    }


@router.get("")
def list_orders(
    request: Request,
    account_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(15, ge=1, le=200),
    db: Session = Depends(get_db),
):
    if account_id is None:
        account = require_account(request, db)
        account_id = account.account_id
    service = OrderService(db)
    paged = service.get_orders(
        account_id=account_id,
        search=search,
        status=status,
        page_number=page,
        page_size=page_size,
    )
    return {
        "items": [_order_to_dict(o) for o in paged],
        "page": paged.current_page,
        "page_size": paged.page_size,
        "total": paged.total_count,
        "total_pages": paged.total_pages,
        "statuses": [s[0] for s in OrderStatus.STATUSES],
    }


@router.get("/{order_id}", response_class=HTMLResponse)
async def order_detail(order_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        account = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)

    order = (
        db.query(Order)
        .filter(Order.order_id == order_id, Order.account_id == account.account_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return templates.TemplateResponse(
        "Orders/detail.html",
        {
            "request": request,
            "page_title": f"Chi tiết đơn hàng #{order.order_id}",
            "order": order,
            "current_user": account,
            "cart_count": _get_cart_count(request, db),
        },
    )


@router.get("/{order_id}/json")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_to_dict(order)


@router.get("/{order_id}/Items")
def get_order_items(order_id: int, db: Session = Depends(get_db)):
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


@router.post("/CreateFromCart")
def create_from_cart(payload: OrderCreateFromCart, db: Session = Depends(get_db)):
    service = OrderService(db)
    try:
        order = service.create_order(
            account_id=payload.account_id,
            customer_name=payload.customer_name,
            customer_phone=payload.customer_phone,
            customer_address=payload.customer_address,
            notes=payload.notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _order_to_dict(order)


@router.post("/Checkout")
def checkout(
    request: Request,
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_address: str = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    account = require_account(request, db)
    service = OrderService(db)
    try:
        order = service.create_order(
            account_id=account.account_id,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            notes=notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _order_to_dict(order)


@router.put("/{order_id}/Status")
def update_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    if payload.status not in [s[0] for s in OrderStatus.STATUSES]:
        raise HTTPException(status_code=400, detail="Invalid status")
    service = OrderService(db)
    order = service.update_order_status(order_id, payload.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_to_dict(order)


@router.post("/{order_id}/Cancel")
def cancel_order(order_id: int, reason: Optional[str] = None, db: Session = Depends(get_db)):
    service = OrderService(db)
    order = service.cancel_order(order_id, reason)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_to_dict(order)
