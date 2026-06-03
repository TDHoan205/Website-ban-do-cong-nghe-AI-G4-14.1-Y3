"""
Home Controller - Trang chủ
Tuong duong Controllers/HomeController.cs trong ASP.NET Core
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Models import Product
from Services.ProductService import ProductService
from Services.CartService import CartService
from Services.AuthService import AuthService
import os, json, time

router = APIRouter()

_LOG_PATH = os.path.join(os.path.dirname(__file__), os.pardir, "debug-ed9600.log")

def _debug_log(session_id: str, hypothesis_id: str, location: str, message: str, data: dict):
    try:
        log_entry = {
            "sessionId": session_id,
            "id": f"log_{int(time.time() * 1000)}",
            "timestamp": int(time.time() * 1000),
            "location": location,
            "message": message,
            "data": data,
            "hypothesisId": hypothesis_id
        }
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


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

    # Query banner products (only iPhone products)
    banner_products = db.query(Product).filter(
        Product.is_available == True,
        Product.name.ilike("%iphone%")
    ).order_by(Product.is_hot.desc(), Product.created_at.desc()).limit(5).all()

    _debug_log("ed9600", "H2", "HomeController.home_index:rendering",
        "Home page rendering - products passed to template",
        {
            "featured_count": len(featured_products) if featured_products else 0,
            "new_count": len(new_products) if new_products else 0,
            "categories_count": len(categories) if categories else 0,
            "banner_products_count": len(banner_products),
            "featured_sample": [
                {
                    "product_id": p.product_id,
                    "name": p.name[:30] if p.name else "",
                    "is_hot": p.is_hot,
                    "is_new": p.is_new,
                    "is_available": p.is_available,
                    "product_image_url": p.image_url,
                    "product_images_count": len(p.product_images) if p.product_images else 0,
                    "product_images": [
                        {"image_id": i.image_id, "image_url": i.image_url, "is_primary": i.is_primary}
                        for i in (p.product_images or [])[:3]
                    ]
                }
                for p in (featured_products or [])[:5]
            ] if featured_products else [],
            "new_sample": [
                {
                    "product_id": p.product_id,
                    "name": p.name[:30] if p.name else "",
                    "product_images_count": len(p.product_images) if p.product_images else 0,
                    "product_images": [
                        {"image_id": i.image_id, "image_url": i.image_url, "is_primary": i.is_primary}
                        for i in (p.product_images or [])[:3]
                    ]
                }
                for p in (new_products or [])[:5]
            ] if new_products else [],
        })

    return templates.TemplateResponse(
        "Home/index.html",
        {
            "request": request,
            "page_title": "Trang chủ",
            "featured_products": featured_products,
            "new_products": new_products,
            "categories": categories,
            "cart_count": cart_count,
            "current_user": current_user,
            "banner_products": banner_products,
            "banner_product": banner_products[0] if banner_products else None,
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
