"""
Cart Controller - Giỏ hàng
Tương đương Controllers/CartController.cs trong ASP.NET Core
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.CartService import CartService
from Utilities.auth import require_account

router = APIRouter(prefix="/Cart")




@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    """Trang giỏ hàng"""
    account = require_account(request, db)

    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(account.account_id)
    items = cart_service.get_cart_items(cart.cart_id)
    total = cart_service.get_cart_total(account.account_id)

    return templates.TemplateResponse(
        "Cart/index.html",
        {
            "request": request,
            "page_title": "Giỏ hàng",
            "cart_items": items,
            "cart_total": total,
            "cart": cart,
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
    account = require_account(request, db)

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
    account = require_account(request, db)

    cart_service = CartService(db)
    cart_service.clear_cart(account.account_id)

    return RedirectResponse(url="/Cart/", status_code=303)


# Templates
templates = None

def set_templates(t):
    global templates
    templates = t
