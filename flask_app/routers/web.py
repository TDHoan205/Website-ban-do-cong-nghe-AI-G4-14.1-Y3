"""
Public website router – home, products, cart, checkout.
All endpoints use real SQL Server database via services.
Prefix: /shop
"""
from fastapi import APIRouter, Request, Query, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..services import ProductService, CartService, OrderService
from ..session import (
    get_session_token, get_session, get_account_id,
    is_authenticated, login,
)
from ..models import Account

from ..app_config import templates


web_router = APIRouter(prefix="/shop", tags=["Website"])


# ── Context builder ──────────────────────────────────────────────────

def _build_context(
    request: Request,
    title: str = "",
    active_controller: str = "",
    db: Optional[Session] = None,
    account_id: int = 0,
) -> dict:
    """Build common template context from DB session."""
    is_auth = is_authenticated(request)
    current_user = None
    is_admin = False
    is_employee = False
    cart_count = 0

    if account_id > 0 and db:
        account = db.query(Account).filter(Account.account_id == account_id).first()
        if account:
            current_user = account.username
            is_admin = account.role and account.role.role_name == "Admin"
            is_employee = account.role and account.role.role_name in ("Admin", "Employee")

    from datetime import datetime
    from ..models import Cart, CartItem
    if account_id > 0 and db:
        cart = db.query(Cart).filter(Cart.account_id == account_id).first()
        if cart:
            cart_count = sum(
                ci.quantity
                for ci in db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).all()
            )

    page_map = {
        "Shop": "home", "Products": "products", "Cart": "cart",
        "Support": "chat", "Profile": "cart", "Orders": "cart",
    }
    active_page = page_map.get(active_controller, active_controller.lower() if active_controller else "")

    return {
        "request": request,
        "app_name": "TechStore",
        "current_year": datetime.now().year,
        "active_page": active_page,
        "active_controller": active_controller,
        "title": title,
        "current_user": current_user,
        "is_admin": is_admin,
        "is_employee": is_employee,
        "is_authenticated": is_auth,
        "cart_count": cart_count,
    }


def _get_account_id(request: Request, response: Response) -> int:
    return get_account_id(request, response, None)


# ── Home page ──────────────────────────────────────────────────────

@web_router.get("/", response_class=HTMLResponse, name="shop.home")
async def home(request: Request, response: Response, db: Session = Depends(get_db)):
    prod_svc = ProductService(db)
    account_id = _get_account_id(request, response)

    categories = prod_svc.get_all_categories()
    new_products = prod_svc.get_new_products(limit=8)
    hot_products = prod_svc.get_hot_products(limit=8)

    ctx = _build_context(request, "Trang chủ", "Shop", db, account_id)
    ctx.update({
        "categories": categories,
        "new_products": new_products,
        "hot_products": hot_products,
    })
    return templates.TemplateResponse("shop/index.html", ctx)


# ── Products listing ──────────────────────────────────────────────────

@web_router.get("/products", response_class=HTMLResponse, name="shop.products")
async def products_list(
    request: Request,
    response: Response,
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort_by: str = Query("newest"),
    filter: Optional[str] = Query(None),
    page: int = Query(1),
    db: Session = Depends(get_db),
):
    prod_svc = ProductService(db)
    account_id = _get_account_id(request, response)

    products, total = prod_svc.search_products(
        query=search or "",
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        page=page,
        page_size=12,
    )
    categories = prod_svc.get_all_categories()
    total_pages = max(1, (total + 11) // 12)

    ctx = _build_context(request, "Sản phẩm", "Products", db, account_id)
    ctx.update({
        "products": products,
        "categories": categories,
        "total_count": total,
        "current_page": page,
        "total_pages": total_pages,
        "has_previous": page > 1,
        "has_next": page < total_pages,
        "search": search or "",
        "category_id": category_id,
        "min_price": min_price,
        "max_price": max_price,
        "sort_by": sort_by,
        "filter": filter or "",
    })
    return templates.TemplateResponse("shop/products.html", ctx)


# ── Product detail ──────────────────────────────────────────────────

@web_router.get("/product/{product_id}", response_class=HTMLResponse, name="shop.product")
async def product_detail(
    request: Request,
    response: Response,
    product_id: int,
    db: Session = Depends(get_db),
):
    prod_svc = ProductService(db)
    account_id = _get_account_id(request, response)

    product = prod_svc.get_product_by_id(product_id)
    if not product:
        ctx = _build_context(request, "Không tìm thấy sản phẩm", "", db, account_id)
        return templates.TemplateResponse("errors/404.html", ctx, status_code=404)

    related = prod_svc.get_related_products(product_id, product.category_id or 0)

    ctx = _build_context(request, product.name, "Products", db, account_id)
    ctx.update({
        "product": product,
        "related_products": related,
    })
    return templates.TemplateResponse("shop/product.html", ctx)


# ── Cart ────────────────────────────────────────────────────────────

@web_router.get("/cart", response_class=HTMLResponse, name="shop.cart")
async def cart_page(request: Request, response: Response, db: Session = Depends(get_db)):
    account_id = _get_account_id(request, response)
    cart_svc = CartService(db)

    cart_items = cart_svc.get_cart(account_id)
    total = cart_svc.get_cart_total(account_id)

    ctx = _build_context(request, "Giỏ hàng", "Cart", db, account_id)
    ctx.update({
        "cart": cart_items,
        "total": total,
    })
    return templates.TemplateResponse("shop/cart.html", ctx)


# ── Checkout ────────────────────────────────────────────────────────

@web_router.get("/checkout", response_class=HTMLResponse, name="shop.checkout")
async def checkout_page(request: Request, response: Response, db: Session = Depends(get_db)):
    account_id = _get_account_id(request, response)
    if not is_authenticated(request):
        return RedirectResponse(url="/auth/login?return_url=/shop/checkout", status_code=302)

    cart_svc = CartService(db)
    cart_items = cart_svc.get_cart(account_id)
    total = cart_svc.get_cart_total(account_id)

    if not cart_items:
        return RedirectResponse(url="/shop/cart", status_code=302)

    ctx = _build_context(request, "Thanh toán", "Cart", db, account_id)
    ctx.update({
        "cart": cart_items,
        "total": total,
    })
    return templates.TemplateResponse("shop/checkout.html", ctx)


@web_router.post("/checkout", name="shop.checkout_submit")
async def checkout_submit(
    request: Request,
    response: Response,
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_address: str = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    account_id = _get_account_id(request, response)

    if not is_authenticated(request):
        return RedirectResponse(url="/auth/login?return_url=/shop/checkout", status_code=302)

    order_svc = OrderService(db)
    cart_svc = CartService(db)
    success, message, order = order_svc.checkout(
        account_id=account_id,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_address=customer_address,
        notes=notes,
    )

    if success:
        return RedirectResponse(url=f"/shop/order-confirmation/{order.order_id}", status_code=302)

    cart_items = cart_svc.get_cart(account_id)
    total = cart_svc.get_cart_total(account_id)
    ctx = _build_context(request, "Thanh toán", "Cart", db, account_id)
    ctx.update({
        "cart": cart_items,
        "total": total,
        "error": message,
    })
    return templates.TemplateResponse("shop/checkout.html", ctx)


# ── Order confirmation ────────────────────────────────────────────────

@web_router.get("/order-confirmation/{order_id}", response_class=HTMLResponse, name="shop.order_confirmation")
async def order_confirmation(
    request: Request,
    response: Response,
    order_id: int,
    db: Session = Depends(get_db),
):
    account_id = _get_account_id(request, response)
    order_svc = OrderService(db)

    order = order_svc.get_order_by_id(order_id)
    if not order:
        ctx = _build_context(request, "Không tìm thấy đơn hàng", "", db, account_id)
        return templates.TemplateResponse("errors/404.html", ctx, status_code=404)

    ctx = _build_context(request, "Xác nhận đơn hàng", "Cart", db, account_id)
    ctx.update({"order": order})
    return templates.TemplateResponse("shop/order_confirmation.html", ctx)


# ── Support ──────────────────────────────────────────────────────────

@web_router.get("/support", response_class=HTMLResponse, name="shop.support")
async def support_page(request: Request, response: Response, db: Session = Depends(get_db)):
    account_id = _get_account_id(request, response)
    ctx = _build_context(request, "Hỗ trợ khách hàng", "Support", db, account_id)
    return templates.TemplateResponse("shop/support.html", ctx)


# ── Orders ──────────────────────────────────────────────────────────

@web_router.get("/orders", response_class=HTMLResponse, name="shop.orders")
async def orders_page(request: Request, response: Response, db: Session = Depends(get_db)):
    account_id = _get_account_id(request, response)
    if not is_authenticated(request):
        return RedirectResponse(url="/auth/login?return_url=/shop/orders", status_code=302)

    order_svc = OrderService(db)
    orders = order_svc.get_orders_by_account(account_id)

    ctx = _build_context(request, "Lịch sử đơn hàng", "Orders", db, account_id)
    ctx.update({"orders": orders})
    return templates.TemplateResponse("shop/order_history.html", ctx)


# ── Profile ─────────────────────────────────────────────────────────

@web_router.get("/profile", response_class=HTMLResponse, name="shop.profile")
async def profile_page(request: Request, response: Response, db: Session = Depends(get_db)):
    account_id = _get_account_id(request, response)
    if not is_authenticated(request):
        return RedirectResponse(url="/auth/login?return_url=/shop/profile", status_code=302)

    ctx = _build_context(request, "Thông tin cá nhân", "Profile", db, account_id)
    account = db.query(Account).filter(Account.account_id == account_id).first()
    ctx.update({"account": account})
    return templates.TemplateResponse("shop/profile.html", ctx)
