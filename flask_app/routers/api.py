"""
API router – cart AJAX endpoints, search, cart count.
All use real SQL Server database via services.
"""
from fastapi import APIRouter, Request, Form, Depends, Response, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..services import ProductService, CartService, OrderService
from ..session import get_account_id, is_authenticated


api_router = APIRouter(prefix="/api", tags=["API"])


# ── Helpers ───────────────────────────────────────────────────────────

def _get_account_id(request: Request, response: Response) -> int:
    """Get account_id from session, creating guest session if needed."""
    return get_account_id(request, response, None)


def _auth_get_account_id(request: Request, response: Response) -> int:
    """Get account_id only if authenticated, else 0."""
    if is_authenticated(request):
        return get_account_id(request, response, None)
    return 0


# ── Search ─────────────────────────────────────────────────────────────

@api_router.get("/search", name="api.search")
async def api_search(
    request: Request,
    response: Response,
    q: str = Query(""),
    db: Session = Depends(get_db),
):
    if len(q) < 2:
        return JSONResponse(content=[])

    prod_svc = ProductService(db)
    products, _ = prod_svc.search_products(query=q, page=1, page_size=8)

    return JSONResponse(content=[
        {
            "productId": p.product_id,
            "name": p.name,
            "price": float(p.price),
            "imageUrl": p.image_url or "",
        }
        for p in products
    ])


# ── Cart count ────────────────────────────────────────────────────────

@api_router.get("/cart/count", name="api.cart_count")
async def api_cart_count(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    account_id = _get_account_id(request, response)
    if account_id == 0:
        return JSONResponse(content=0)

    cart_svc = CartService(db)
    count = cart_svc.get_cart_count(account_id)
    return JSONResponse(content=count)


# ── Add to cart ───────────────────────────────────────────────────────

@api_router.post("/cart/add", name="api.cart_add")
async def api_add_to_cart(
    request: Request,
    response: Response,
    productId: int = Form(...),
    quantity: int = Form(1),
    variantId: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    account_id = _get_account_id(request, response)

    if account_id == 0:
        # Guest – require login
        return JSONResponse(content={
            "success": False,
            "requiresLogin": True,
            "message": "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.",
        })

    cart_svc = CartService(db)
    success, message = cart_svc.add_item(
        account_id=account_id,
        product_id=productId,
        quantity=quantity,
        variant_id=variantId,
    )

    return JSONResponse(content={
        "success": success,
        "message": message,
        "requiresLogin": False,
    })


# ── Update cart item ─────────────────────────────────────────────────

@api_router.post("/cart/update", name="api.cart_update")
async def api_update_cart(
    request: Request,
    response: Response,
    productId: int = Form(...),
    quantity: int = Form(...),
    variantId: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    account_id = _auth_get_account_id(request, response)
    if account_id == 0:
        return JSONResponse(content={"success": False, "message": "Vui lòng đăng nhập."})

    cart_svc = CartService(db)
    success, message, new_qty = cart_svc.update_item_quantity(
        account_id=account_id,
        product_id=productId,
        quantity=quantity,
        variant_id=variantId,
    )

    return JSONResponse(content={
        "success": success,
        "message": message,
        "newQuantity": new_qty,
        "cartTotal": cart_svc.get_cart_total(account_id),
    })


# ── Remove from cart ────────────────────────────────────────────────

@api_router.post("/cart/remove", name="api.cart_remove")
async def api_remove_from_cart(
    request: Request,
    response: Response,
    productId: int = Form(...),
    variantId: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    account_id = _auth_get_account_id(request, response)
    if account_id == 0:
        return JSONResponse(content={"success": False, "message": "Vui lòng đăng nhập."})

    cart_svc = CartService(db)
    success = cart_svc.remove_item(
        account_id=account_id,
        product_id=productId,
        variant_id=variantId,
    )

    return JSONResponse(content={
        "success": success,
        "cartTotal": cart_svc.get_cart_total(account_id),
    })


# ── Clear cart ───────────────────────────────────────────────────────

@api_router.post("/cart/clear", name="api.cart_clear")
async def api_clear_cart(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    account_id = _auth_get_account_id(request, response)
    if account_id == 0:
        return JSONResponse(content={"success": False})

    cart_svc = CartService(db)
    cart_svc.clear_cart(account_id)
    return JSONResponse(content={"success": True})
