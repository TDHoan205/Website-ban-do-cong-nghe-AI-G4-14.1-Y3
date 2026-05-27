"""
Products Controller - Quan ly san pham
Tuong duong Controllers/ProductsController.cs trong ASP.NET Core
"""
import json
from typing import Optional, List
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.ProductService import ProductService
from Services.CartService import CartService
from Services.AuthService import AuthService
from Utilities.auth import require_account
from Utilities.http import is_ajax_request, safe_redirect_url

router = APIRouter(prefix="/Products")


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
    category_id: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    discount: Optional[int] = Query(None),
    sort: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    storage: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    # Normalize: empty strings / "None" string / whitespace-only → None
    _category_id_raw = category_id
    try:
        _cid = category_id.strip() if category_id else ""
        category_id_int = int(_cid) if _cid and _cid.lower() not in ("", "none", "null") else None
    except (ValueError, TypeError):
        category_id_int = None

    _search_raw = search
    search = search.strip() if search else None
    if search in ("", "None", "null"):
        search = None

    _page_raw = page
    if page < 1:
        page = 1

    print(f"[Products/index] category_id={category_id_int!r}  search={search!r}  "
          f"sort_by={sort_by!r}  storage={storage!r}  page={page}")
    product_service = ProductService(db)

    is_new = False
    is_hot = False
    if sort == "new":
        is_new = True
    elif sort == "hot":
        is_hot = True

    products, total = product_service.get_all_products(
        category_id=category_id_int,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size,
        min_price=min_price,
        max_price=max_price,
        discount=(discount == 1),
        is_new=is_new,
        is_hot=is_hot,
        storage=storage,
    )
    categories = product_service.get_all_categories()
    storage_counts = product_service.get_storage_counts(category_id=category_id_int)

    category_name = None
    if category_id_int:
        cat = product_service.get_category_by_id(category_id_int)
        if cat:
            category_name = cat.name

    cart_count = _get_cart_count(request, db)
    current_user = _get_current_user(request, db)

    return templates.TemplateResponse(
        "Products/index.html",
        {
            "request": request,
            "page_title": category_name or "Tất cả sản phẩm",
            "category_name": category_name,
            "products": products,
            "categories": categories,
            "total_products": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size if total > 0 else 1,
            "category_id": category_id_int,
            "search": search or "",
            "sort_by": sort_by,
            "sort_order": sort_order,
            "min_price": min_price or "",
            "max_price": max_price or "",
            "cart_count": cart_count,
            "current_user": current_user,
            "storage_counts": storage_counts,
            "selected_storages": storage or [],
        }
    )


@router.get("/{product_id}", response_class=HTMLResponse)
async def detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    product = product_service.get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Sản phẩm không tìm thấy")

    # Parse specifications JSON từ database
    specifications_dict = {}
    if product.specifications:
        try:
            specifications_dict = json.loads(product.specifications)
            if not isinstance(specifications_dict, dict):
                specifications_dict = {}
        except Exception:
            specifications_dict = {}

    related = product_service.get_related_products(
        product_id, product.category_id if product.category_id else 0
    )

    # Safe load variants + images using separate queries
    try:
        from Models.Product import ProductVariant, ProductImage
        variants_list = db.query(ProductVariant).filter(
            ProductVariant.product_id == product_id
        ).all()
        all_images = db.query(ProductImage).filter(
            ProductImage.product_id == product_id
        ).all()
    except Exception:
        variants_list = []
        all_images = []

    variants_data = []
    for v in variants_list:
        is_active = getattr(v, 'is_active', True)
        if is_active == False:
            continue
        var_imgs = [i for i in all_images if getattr(i, 'variant_id', None) == v.variant_id]
        if not var_imgs:
            var_imgs = [i for i in all_images if not getattr(i, 'variant_id', None)]
        variants_data.append({
            "variant_id": v.variant_id,
            "color": v.color or "",
            "color_hex": getattr(v, 'color_hex', "") or "",
            "storage": v.storage or "",
            "ram": v.ram or "",
            "variant_name": v.variant_name or "",
            "price": float(v.price) if v.price else None,
            "original_price": float(v.original_price) if v.original_price else None,
            "stock_quantity": getattr(v, 'stock_quantity', 0) or 0,
            "is_active": is_active,
            "images": [
                {"image_url": i.image_url, "is_primary": i.is_primary}
                for i in var_imgs
            ]
        })

    product_images = [
        {"image_id": i.image_id, "image_url": i.image_url, "is_primary": i.is_primary}
        for i in all_images if not getattr(i, 'variant_id', None)
    ]

    current_user = _get_current_user(request, db)

    return templates.TemplateResponse(
        "Products/detail.html",
        {
            "request": request,
            "page_title": product.name,
            "product": product,
            "specifications_dict": specifications_dict,
            "variants": variants_data,
            "product_images": product_images,
            "related_products": related,
            "current_user": current_user,
        }
    )


@router.post("/{product_id}/add-to-cart")
async def add_to_cart(
    request: Request,
    product_id: int,
    quantity: int = Form(1, ge=1),
    variant_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        account = require_account(request, db)
    except HTTPException:
        if is_ajax_request(request):
            return JSONResponse(
                {"success": False, "message": "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.", "login_url": "/Auth/Login"},
                status_code=401,
            )
        return RedirectResponse(url="/Auth/Login", status_code=303)

    cart_service = CartService(db)
    cart_service.add_item(account.account_id, product_id, quantity, variant_id)
    cart_count = cart_service.get_cart_item_count(account.account_id)

    if is_ajax_request(request):
        return JSONResponse(
            {"success": True, "message": "Đã thêm sản phẩm vào giỏ hàng.", "cart_count": cart_count},
            status_code=200
        )

    referer = request.headers.get("referer")
    return RedirectResponse(url=referer or f"/Products/{product_id}", status_code=303)


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
