"""
Home Controller - Trang chủ
Tương đương Controllers/HomeController.cs trong ASP.NET Core
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.ProductService import ProductService

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home_index(request: Request, db: Session = Depends(get_db)):
    """
    Trang chủ - Hiển thị sản phẩm nổi bật và mới
    """
    product_service = ProductService(db)

    featured_products = product_service.get_featured_products(8)
    new_products = product_service.get_new_products(8)
    categories = product_service.get_all_categories()

    return templates.TemplateResponse(
        "Home/index.html",
        {
            "request": request,
            "page_title": "Trang chủ",
            "featured_products": featured_products,
            "new_products": new_products,
            "categories": categories,
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


# Templates sẽ được gán từ app.py
templates = None

def set_templates(t):
    global templates
    templates = t
