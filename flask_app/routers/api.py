"""
API routes – AJAX endpoints for cart, search, etc.
"""
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import JSONResponse
from typing import Optional
import json

from ..services import (
    search_products, get_or_create_session, get_session,
    add_to_cart, update_cart_item, remove_from_cart,
    get_cart_count, get_cart, get_cart_total,
    clear_cart,
)

api_router = APIRouter(prefix="/api", tags=["API"])


@api_router.get("/search", name="api.search")
async def api_search(q: str = ""):
    if len(q) < 2:
        return JSONResponse(content=[])
    products = search_products(q)[:8]
    return JSONResponse(content=[
        {
            "productId": p.product_id,
            "name": p.name,
            "price": p.price,
            "imageUrl": p.image_url or "",
        }
        for p in products
    ])


@api_router.get("/cart/count", name="api.cart_count")
async def api_cart_count(request: Request):
    sid = request.cookies.get("session_id", "")
    count = get_cart_count(sid) if sid else 0
    return JSONResponse(content=count)


@api_router.post("/cart/add", name="api.cart_add")
async def api_add_to_cart(
    request: Request,
    response: Response,
    productId: int = Form(...),
    quantity: int = Form(1),
    variantId: Optional[int] = Form(None),
):
    sid, _ = get_or_create_session(request.cookies.get("session_id"))

    # Ensure session cookie
    success = add_to_cart(sid, productId, quantity, variantId)
    resp = JSONResponse(content={
        "success": success,
        "message": "Đã thêm vào giỏ hàng!" if success else "Không thể thêm sản phẩm.",
    })
    resp.set_cookie("session_id", sid, httponly=True, samesite="lax", max_age=86400)
    return resp


@api_router.post("/cart/update", name="api.cart_update")
async def api_update_cart(
    request: Request,
    response: Response,
    productId: int = Form(...),
    quantity: int = Form(...),
    variantId: Optional[int] = Form(None),
):
    sid, _ = get_or_create_session(request.cookies.get("session_id"))
    new_qty = update_cart_item(sid, productId, quantity, variantId)

    resp = JSONResponse(content={
        "success": True,
        "newQuantity": new_qty,
        "cartTotal": get_cart_total(sid),
    })
    resp.set_cookie("session_id", sid, httponly=True, samesite="lax", max_age=86400)
    return resp


@api_router.post("/cart/remove", name="api.cart_remove")
async def api_remove_from_cart(
    request: Request,
    response: Response,
    productId: int = Form(...),
    variantId: Optional[int] = Form(None),
):
    sid, _ = get_or_create_session(request.cookies.get("session_id"))
    remove_from_cart(sid, productId, variantId)

    resp = JSONResponse(content={
        "success": True,
        "cartTotal": get_cart_total(sid),
    })
    resp.set_cookie("session_id", sid, httponly=True, samesite="lax", max_age=86400)
    return resp
