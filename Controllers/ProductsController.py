"""
Products Controller - Quản lý sản phẩm
Tương đương Controllers/ProductsController.cs trong ASP.NET Core
"""
from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.ProductService import ProductService
from Services.CartService import CartService
from Utilities.auth import require_account

router = APIRouter(prefix="/Products")




class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    stock_quantity: Optional[int] = 0
    is_available: Optional[bool] = True
    is_new: Optional[bool] = False
    is_hot: Optional[bool] = False
    discount_percent: Optional[int] = 0
    specifications: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    is_available: Optional[bool] = None
    is_new: Optional[bool] = None
    is_hot: Optional[bool] = None
    discount_percent: Optional[int] = None
    specifications: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    category_id: int = Query(None),
    search: str = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Danh sách sản phẩm có phân trang, lọc, tìm kiếm"""
    product_service = ProductService(db)

    products, total = product_service.get_all_products(
        category_id=category_id,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )
    categories = product_service.get_all_categories()

    return templates.TemplateResponse(
        "Products/index.html",
        {
            "request": request,
            "page_title": "Sản phẩm",
            "products": products,
            "categories": categories,
            "total_products": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "category_id": category_id,
            "search": search,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
    )


@router.get("/{product_id}", response_class=HTMLResponse)
async def detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    """Chi tiết sản phẩm"""
    product_service = ProductService(db)
    product = product_service.get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tìm thấy")

    related = product_service.get_related_products(
        product_id, product.category_id if product.category_id else 0
    )

    return templates.TemplateResponse(
        "Products/detail.html",
        {
            "request": request,
            "page_title": product.name,
            "product": product,
            "related_products": related,
        }
    )


@router.post("/{product_id}/add-to-cart")
async def add_to_cart(
    request: Request,
    product_id: int,
    quantity: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """Thêm sản phẩm vào giỏ hàng"""
    account = require_account(request, db)

    cart_service = CartService(db)
    cart_service.add_item(account.account_id, product_id, quantity)

    return RedirectResponse(url="/Cart/", status_code=303)


@router.get("/Admin")
async def admin_list(
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    sort_order: str = Query("name"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db)
):
    service = ProductService(db)
    paged = service.get_all_products_admin(
        search=search,
        category_id=category_id,
        sort_order=sort_order,
        page_number=page,
        page_size=page_size,
    )
    return {
        "items": [
            {
                "product_id": p.product_id,
                "name": p.name,
                "price": float(p.price),
                "stock_quantity": p.stock_quantity,
                "is_available": p.is_available,
                "category_id": p.category_id,
                "supplier_id": p.supplier_id,
            }
            for p in paged
        ],
        "page": paged.current_page,
        "page_size": paged.page_size,
        "total": paged.total_count,
        "total_pages": paged.total_pages,
    }


@router.post("/Admin")
async def admin_create(payload: ProductCreate, db: Session = Depends(get_db)):
    if not payload.name.strip():
        raise HTTPException(status_code=400, detail="Product name is required")
    if payload.price is None or payload.price < 0:
        raise HTTPException(status_code=400, detail="Invalid price")
    service = ProductService(db)
    product = service.create_product(payload.model_dump())
    return {"product_id": product.product_id}


@router.put("/Admin/{product_id}")
async def admin_update(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_unset=True)
    if "name" in data and not data["name"].strip():
        raise HTTPException(status_code=400, detail="Product name is required")
    if "price" in data and data["price"] is not None and data["price"] < 0:
        raise HTTPException(status_code=400, detail="Invalid price")
    service = ProductService(db)
    product = service.update_product(product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True}


@router.delete("/Admin/{product_id}")
async def admin_delete(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    ok = service.delete_product(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True}


# Templates
templates = None

def set_templates(t):
    global templates
    templates = t
