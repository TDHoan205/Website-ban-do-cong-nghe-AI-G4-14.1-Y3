"""
Admin router – dashboard and management pages using real SQL Server database.
"""
from fastapi import APIRouter, Request, Query, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..services import ProductService, OrderService
from ..session import is_authenticated, get_account_id
from ..models import Account

from ..app_config import templates


admin_router = APIRouter(prefix="/admin", tags=["Admin"])


def _require_auth(request: Request, db: Session):
    """Return account if authenticated, else None."""
    if not is_authenticated(request):
        return None
    token = request.cookies.get("session_token")
    if not token:
        return None
    from ..session import get_session
    sess = get_session(token)
    if not sess or sess["account_id"] <= 0:
        return None
    return db.query(Account).filter(Account.account_id == sess["account_id"]).first()


def _is_admin(account: Optional[Account]) -> bool:
    if not account:
        return False
    return account.role and account.role.role_name == "Admin"


def _is_employee(account: Optional[Account]) -> bool:
    if not account:
        return False
    return account.role and account.role.role_name in ("Admin", "Employee")


def _admin_context(
    request: Request,
    db: Session,
    title: str = "",
    active_controller: str = "",
):
    account = _require_auth(request, db)
    if not account:
        return None

    return {
        "request": request,
        "title": title,
        "active_controller": active_controller,
        "current_user": account.username,
        "is_admin": _is_admin(account),
        "is_employee": _is_employee(account),
        "app_name": "TechStore",
    }


# ── Dashboard ───────────────────────────────────────────────

@admin_router.get("/", response_class=HTMLResponse, name="admin.dashboard")
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    ctx = _admin_context(request, db, "Dashboard", "Dashboard")
    if ctx is None:
        return RedirectResponse(url="/auth/login", status_code=302)

    order_svc = OrderService(db)
    prod_svc = ProductService(db)

    orders = order_svc.get_all_orders()
    products = prod_svc.get_all_products()

    from datetime import datetime, timedelta
    today = datetime.now().date()

    # Stats
    today_orders = [o for o in orders if o.order_date.date() == today]
    total_revenue = sum(float(o.total_amount) for o in orders)
    today_revenue = sum(float(o.total_amount) for o in today_orders)
    pending_orders = [o for o in orders if o.status == "Pending"]

    ctx.update({
        "stats": {
            "total_orders": len(orders),
            "today_orders": len(today_orders),
            "total_revenue": total_revenue,
            "today_revenue": today_revenue,
            "pending_orders": len(pending_orders),
            "total_products": len(products),
        },
        "recent_orders": orders[:10],
    })

    return templates.TemplateResponse("admin/dashboard.html", ctx)


# ── Products ─────────────────────────────────────────────────

@admin_router.get("/products", response_class=HTMLResponse, name="admin.products")
async def admin_products(request: Request, db: Session = Depends(get_db)):
    ctx = _admin_context(request, db, "Quản lý sản phẩm", "Products")
    if ctx is None:
        return RedirectResponse(url="/auth/login", status_code=302)

    prod_svc = ProductService(db)
    products = prod_svc.get_all_products()
    categories = prod_svc.get_all_categories()

    ctx.update({
        "products": products,
        "categories": categories,
    })
    return templates.TemplateResponse("admin/products/index.html", ctx)


# ── Categories ───────────────────────────────────────────────

@admin_router.get("/categories", response_class=HTMLResponse, name="admin.categories")
async def admin_categories(request: Request, db: Session = Depends(get_db)):
    ctx = _admin_context(request, db, "Quản lý danh mục", "Categories")
    if ctx is None:
        return RedirectResponse(url="/auth/login", status_code=302)

    prod_svc = ProductService(db)
    categories = prod_svc.get_all_categories()

    ctx.update({"categories": categories})
    return templates.TemplateResponse("admin/categories/index.html", ctx)


# ── Orders ─────────────────────────────────────────────────

@admin_router.get("/orders", response_class=HTMLResponse, name="admin.orders")
async def admin_orders(request: Request, db: Session = Depends(get_db)):
    ctx = _admin_context(request, db, "Quản lý đơn hàng", "Orders")
    if ctx is None:
        return RedirectResponse(url="/auth/login", status_code=302)

    order_svc = OrderService(db)
    orders = order_svc.get_all_orders()

    ctx.update({"orders": orders})
    return templates.TemplateResponse("admin/orders/index.html", ctx)


# ── Accounts ────────────────────────────────────────────────

@admin_router.get("/accounts", response_class=HTMLResponse, name="admin.accounts")
async def admin_accounts(request: Request, db: Session = Depends(get_db)):
    ctx = _admin_context(request, db, "Quản lý tài khoản", "Accounts")
    if ctx is None:
        return RedirectResponse(url="/auth/login", status_code=302)

    accounts = db.query(Account).all()
    ctx.update({"accounts": accounts})
    return templates.TemplateResponse("admin/accounts/index.html", ctx)
