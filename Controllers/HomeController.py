"""
Home Controller - Trang chủ
Tuong duong Controllers/HomeController.cs trong ASP.NET Core
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.ProductService import ProductService
from Services.CartService import CartService
from Services.AuthService import AuthService

router = APIRouter()


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


def _get_current_user(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    auth_service = AuthService(db)
    return auth_service.get_current_account_from_token(token)


@router.get("/", response_class=HTMLResponse)
async def home_index(request: Request, db: Session = Depends(get_db)):
    """
    Trang chu - Hien thi san pham noi bat va moi
    """
    product_service = ProductService(db)

    featured_products = product_service.get_featured_products(8)
    new_products = product_service.get_new_products(8)
    categories = product_service.get_all_categories()
    cart_count = _get_cart_count(request, db)
    current_user = _get_current_user(request, db)

    return templates.TemplateResponse(
        "Home/index.html",
        {
            "request": request,
            "page_title": "Trang chu",
            "featured_products": featured_products,
            "new_products": new_products,
            "categories": categories,
            "cart_count": cart_count,
            "current_user": current_user,
        }
    )


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Trang giới thiệu"""
    return templates.TemplateResponse(
        "Home/about.html",
        {"request": request, "page_title": "Giới thiệu"}
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Trang liên hệ"""
    return templates.TemplateResponse(
        "Home/contact.html",
        {"request": request, "page_title": "Liên hệ"}
    )


# Templates se duoc gan tu app.py
templates = None

def set_templates(t):
    global templates
    templates = t
