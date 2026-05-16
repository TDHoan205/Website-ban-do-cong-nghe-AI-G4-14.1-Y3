"""
Cart Controller - Giỏ hàng
Tuong duong Controllers/CartController.cs trong ASP.NET Core
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.CartService import CartService
from Services.AuthService import AuthService
from Utilities.auth import require_account

router = APIRouter(prefix="/Cart")


def _get_cart_count(request: Request, db: Session) -> int:
    token = request.cookies.get("access_token")
    if not token:
        return 0
    auth_service = AuthService(db)
    account = auth_service.get_current_account_from_token(token)
    if not account:
        return 0
    cart_service = CartService(db)
    return cart_service.get_cart_item_count(account.account_id)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    """Trang giỏ hàng"""
    try:
        account = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)

    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(account.account_id)
    items = cart_service.get_cart_items(cart.cart_id)
    total = cart_service.get_cart_total(account.account_id)
    cart_count = _get_cart_count(request, db)

    return templates.TemplateResponse(
        "Cart/index.html",
        {
            "request": request,
            "page_title": "Giỏ hàng",
            "cart_items": items,
            "cart_total": total,
            "cart": cart,
            "cart_count": cart_count,
        }
    )


@router.post("/add")
async def add(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(1),
    db: Session = Depends(get_db)
):
    """Thêm sản phẩm vào giỏ hàng"""
    try:
        account = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)

    cart_service = CartService(db)
    cart_service.add_item(account.account_id, product_id, quantity)

    return RedirectResponse(url="/Cart/", status_code=303)


@router.post("/update/{item_id}")
async def update(
    item_id: int,
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    """Cập nhật số lượng"""
    cart_service = CartService(db)
    cart_service.update_item_quantity(item_id, quantity)
    return RedirectResponse(url="/Cart/", status_code=303)


@router.post("/remove/{item_id}")
async def remove(item_id: int, db: Session = Depends(get_db)):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart_service = CartService(db)
    cart_service.remove_item(item_id)
    return RedirectResponse(url="/Cart/", status_code=303)


@router.post("/clear")
async def clear(request: Request, db: Session = Depends(get_db)):
    """Xóa toàn bộ giỏ hàng"""
    try:
        account = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)

    cart_service = CartService(db)
    cart_service.clear_cart(account.account_id)

    return RedirectResponse(url="/Cart/", status_code=303)


# Templates
templates = None

def set_templates(t):
    global templates
    templates = t
