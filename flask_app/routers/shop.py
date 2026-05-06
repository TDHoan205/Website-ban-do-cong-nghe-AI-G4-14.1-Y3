"""
Shop routes – public-facing storefront.
"""
from ..app_config import templates
from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from datetime import datetime
from typing import Optional

from ..services import (
    get_all_products, get_product_by_id, get_new_products, get_hot_products,
    search_products, paginate_products, get_all_categories,
    get_cart, get_cart_count, get_cart_total,
    add_to_cart, update_cart_item, remove_from_cart, clear_cart,
    get_or_create_session, get_session,
    authenticate,
)

shop_router = APIRouter(prefix="", tags=["Shop"])


def _session_id(request: Request) -> str:
    return request.cookies.get("session_id", "")


def _make_context(request: Request, title: str = "", active_controller: str = "",
                  extra: Optional[dict] = None):
    sid = _session_id(request)
    session = get_session(sid)
    cart = get_cart(sid)
    ctx = {
        "app_name": "TechStore",
        "current_year": datetime.now().year,
        "title": title,
        "active_controller": active_controller,
        "current_user": session.get("username"),
        "is_admin": session.get("role") == "Admin",
        "is_employee": session.get("role") in ("Admin", "Employee"),
        "cart_count": len(cart),
    }
    if extra:
        ctx.update(extra)
    return ctx


# ─── Landing page (/) ────────────────────────────────────
# REMOVED – served by web_router at /


# ─── Shop index ─────────────────────────────────────────
@shop_router.get("/shop", response_class=HTMLResponse, name="shop.index")
async def shop_index(request: Request):
    categories = get_all_categories()
    new_products = get_new_products()
    hot_products = get_hot_products()
    all_products = get_all_products()

    ctx = _make_context(request, "Trang chủ", active_controller="Shop")
    ctx.update({
        "categories": categories,
        "new_products": new_products,
        "hot_products": hot_products,
        "all_products": all_products,
    })
    return templates.TemplateResponse("shop/index.html", {"request": request, **ctx})


# ─── Products listing ────────────────────────────────────
@shop_router.get("/shop/products", response_class=HTMLResponse, name="shop.products")
async def shop_products(
    request: Request,
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort_by: str = Query("newest"),
    filter_: Optional[str] = Query(None, alias="filter"),
    page: int = Query(1),
):
    all_p = get_all_products()
    if filter_ == "new":
        all_p = get_new_products()
    elif filter_ == "hot":
        all_p = get_hot_products()

    categories = get_all_categories()
    result = paginate_products(
        products=all_p,
        page=page, page_size=8,
        search=search, category_id=category_id,
        min_price=min_price, max_price=max_price,
        sort_by=sort_by,
    )

    ctx = _make_context(request, "Sản phẩm", active_controller="Products")
    ctx.update({
        "categories": categories,
        "products": result.items,
        "total_count": result.total_count,
        "current_page": result.current_page,
        "total_pages": result.total_pages,
        "has_previous": result.has_previous,
        "has_next": result.has_next,
        "search": search or "",
        "category_id": category_id,
        "min_price": min_price,
        "max_price": max_price,
        "sort_by": sort_by,
        "filter": filter_ or "",
    })
    return templates.TemplateResponse("shop/products.html", {"request": request, **ctx})


# ─── Product detail ──────────────────────────────────────
@shop_router.get("/shop/product/{product_id}", response_class=HTMLResponse, name="shop.product")
async def shop_product(request: Request, product_id: int):
    product = get_product_by_id(product_id)
    if not product:
        return templates.TemplateResponse("errors/404.html",
                                        {"request": request, "title": "Not Found"})
    ctx = _make_context(request, product.name, active_controller="Products")
    ctx.update({"product": product})
    return templates.TemplateResponse("shop/product.html", {"request": request, **ctx})


# ─── Cart ────────────────────────────────────────────────
@shop_router.get("/shop/cart", response_class=HTMLResponse, name="shop.cart")
async def shop_cart(request: Request):
    sid = _session_id(request)
    cart = get_cart(sid)
    total = get_cart_total(sid)
    ctx = _make_context(request, "Giỏ hàng", active_controller="Cart")
    ctx.update({"cart": cart, "total": total})
    return templates.TemplateResponse("shop/cart.html", {"request": request, **ctx})


# ─── Order detail ────────────────────────────────────────
@shop_router.get("/shop/order/{order_id}", response_class=HTMLResponse, name="shop.order_detail")
async def shop_order_detail(request: Request, order_id: int):
    from ..services import get_order_by_id
    order = get_order_by_id(order_id)
    ctx = _make_context(request, f"Đơn hàng #{order_id}", active_controller="Orders")
    ctx.update({"order": order})
    return templates.TemplateResponse("shop/order_detail.html", {"request": request, **ctx})


# ─── Order history ───────────────────────────────────────
@shop_router.get("/shop/orders", response_class=HTMLResponse, name="shop.order_history")
async def shop_order_history(request: Request):
    from ..services import get_all_orders
    orders = get_all_orders()
    ctx = _make_context(request, "Lịch sử đơn hàng", active_controller="Orders")
    ctx.update({"orders": orders})
    return templates.TemplateResponse("shop/order_history.html", {"request": request, **ctx})


# ─── Profile ─────────────────────────────────────────────
@shop_router.get("/shop/profile", response_class=HTMLResponse, name="shop.profile")
async def shop_profile(request: Request):
    ctx = _make_context(request, "Thông tin cá nhân", active_controller="Profile")
    return templates.TemplateResponse("shop/profile.html", {"request": request, **ctx})


# ─── Support ─────────────────────────────────────────────
@shop_router.get("/shop/support", response_class=HTMLResponse, name="shop.support")
async def shop_support(request: Request):
    ctx = _make_context(request, "Hỗ trợ", active_controller="Support")
    return templates.TemplateResponse("shop/support.html", {"request": request, **ctx})


# ─── Checkout (placeholder) ─────────────────────────────
@shop_router.get("/shop/checkout", response_class=HTMLResponse, name="shop.checkout")
async def shop_checkout(request: Request):
    sid = _session_id(request)
    cart = get_cart(sid)
    if not cart:
        return RedirectResponse(url="/shop/cart", status_code=302)
    total = get_cart_total(sid)
    ctx = _make_context(request, "Thanh toán", active_controller="Cart")
    ctx.update({"cart": cart, "total": total})
    return templates.TemplateResponse("shop/checkout.html", {"request": request, **ctx})


# ─── Legacy /shop/ redirects (keep for backwards compat) ─────────
@shop_router.get("/shop", name="shop.legacy_index")
async def shop_legacy(request: Request):
    return RedirectResponse(url="/", status_code=301)
