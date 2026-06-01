"""
Cart Controller - Giỏ hàng
Tuong duong Controllers/CartController.cs trong ASP.NET Core
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.CartService import CartService
from Services.AuthService import AuthService
from Utilities.auth import require_account
from Utilities.http import is_ajax_request, safe_redirect_url

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


def _get_current_user(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    auth_service = AuthService(db)
    return auth_service.get_current_account_from_token(token)


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
    current_user = _get_current_user(request, db)

    return templates.TemplateResponse(
        "Cart/index.html",
        {
            "request": request,
            "page_title": "Giỏ hàng",
            "cart_items": items,
            "cart_total": total,
            "cart": cart,
            "cart_count": cart_count,
            "current_user": current_user,
        }
    )


@router.get("/Count")
async def count(request: Request, db: Session = Depends(get_db)):
    """Lay so luong san pham trong gio hang"""
    return {"count": _get_cart_count(request, db)}


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
        if is_ajax_request(request):
            return JSONResponse(
                {"success": False, "message": "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.", "login_url": "/Auth/Login"},
                status_code=401,
            )
        return RedirectResponse(url="/Auth/Login", status_code=303)

    cart_service = CartService(db)
    result = cart_service.add_item(account.account_id, product_id, quantity)
    cart_count = cart_service.get_cart_item_count(account.account_id)

    if is_ajax_request(request):
        if result.success:
            return JSONResponse(
                {"success": True, "message": result.message, "cart_count": cart_count},
                status_code=200
            )
        else:
            return JSONResponse(
                {"success": False, "message": result.message},
                status_code=400
            )

    referer = request.headers.get("referer")
    return RedirectResponse(url=referer or "/Cart/", status_code=303)


@router.post("/update/{item_id}")
async def update(
    item_id: int,
    quantity: int = Form(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Cập nhật số lượng"""
    cart_service = CartService(db)
    cart_service.update_item_quantity(item_id, quantity)
    if request and is_ajax_request(request):
        return JSONResponse({"success": True}, status_code=200)
    return RedirectResponse(url="/Cart/", status_code=303)


@router.get("/update-variant-data/{item_id}")
async def get_cart_item_variant_data(item_id: int, db: Session = Depends(get_db)):
    """API trả về thông tin variant + product của 1 cart item (dùng cho modal sửa option)"""
    from Models.Cart import CartItem
    item = db.query(CartItem).filter(CartItem.cart_item_id == item_id).first()
    if not item:
        return JSONResponse({"success": False, "message": "Item not found"}, status_code=404)

    try:
        from Models.Product import ProductVariant, ProductImage
        variants_list = db.query(ProductVariant).filter(
            ProductVariant.product_id == item.product_id,
            ProductVariant.is_active == True
        ).all()
        all_images = db.query(ProductImage).filter(
            ProductImage.product_id == item.product_id
        ).all()
    except Exception:
        variants_list = []
        all_images = []

    variants_data = []
    for v in variants_list:
        var_imgs = [i for i in all_images if getattr(i, 'variant_id', None) == v.variant_id]
        if not var_imgs:
            var_imgs = [i for i in all_images if not getattr(i, 'variant_id', None)]
        variants_data.append({
            "variant_id": v.variant_id,
            "color": v.color or "",
            "color_hex": getattr(v, 'color_hex', "") or "",
            "storage": v.storage or "",
            "variant_name": v.variant_name or "",
            "price": float(v.price) if v.price else None,
            "stock_quantity": getattr(v, 'stock_quantity', 0) or 0,
            "images": [
                {"image_url": i.image_url, "is_primary": i.is_primary}
                for i in var_imgs
            ]
        })

    product_data = None
    if item.product:
        product_data = {
            "product_id": item.product.product_id,
            "name": item.product.name,
            "price": float(item.product.price),
            "image_url": item.product.image_url,
            "first_image_url": item.product.first_image_url,
        }

    return JSONResponse({
        "success": True,
        "item": {
            "cart_item_id": item.cart_item_id,
            "quantity": item.quantity,
            "variant_id": item.variant_id,
        },
        "product": product_data,
        "variants": variants_data,
    })


@router.post("/update-variant/{item_id}")
async def update_variant(
    item_id: int,
    variant_id: int = Form(...),
    quantity: int = Form(1),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Cập nhật variant và số lượng của cart item"""
    cart_service = CartService(db)
    cart_service.update_item_variant(item_id, variant_id, quantity)
    if request and is_ajax_request(request):
        return JSONResponse({"success": True, "message": "Đã cập nhật option sản phẩm."}, status_code=200)
    return RedirectResponse(url="/Cart/", status_code=303)


@router.post("/remove/{item_id}")
async def remove(item_id: int, request: Request = None, db: Session = Depends(get_db)):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart_service = CartService(db)
    cart_service.remove_item(item_id)
    if request and is_ajax_request(request):
        return JSONResponse({"success": True}, status_code=200)
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
