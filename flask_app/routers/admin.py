"""
Admin routes – dashboard and management pages.
"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional

from ..app_config import templates
from ..services import (
    get_session, get_dashboard_stats, get_all_products,
    get_all_categories, get_all_suppliers, get_all_accounts,
    get_all_orders, get_or_create_session,
)

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


def _admin_context(request: Request, title: str = "", active_controller: str = ""):
    session_id = request.cookies.get("session_id", "")
    session = get_session(session_id) if session_id else {}
    username = session.get("username")
    if not username:
        return None  # not logged in

    return {
        "title": title,
        "active_controller": active_controller,
        "current_user": username,
        "is_admin": session.get("role") == "Admin",
        "is_employee": session.get("role") in ("Admin", "Employee"),
    }


def _require_auth(request: Request):
    session_id = request.cookies.get("session_id", "")
    session = get_session(session_id) if session_id else {}
    return session.get("username") is not None


# ─── Dashboard ────────────────────────────────────────────
@admin_router.get("/", response_class=HTMLResponse, name="admin.dashboard")
async def admin_dashboard(request: Request):
    if not _require_auth(request):
        return RedirectResponse(url="/auth/login", status_code=302)

    ctx = _admin_context(request, "Dashboard", "Dashboard")
    if ctx is None:
        return RedirectResponse(url="/auth/login", status_code=302)

    stats = get_dashboard_stats()
    ctx.update({
        "stats": stats,
        "top_products": stats.top_products,
        "recent_orders": stats.recent_orders,
        "revenue_by_day": stats.revenue_by_day,
    })
    return templates.TemplateResponse("admin/dashboard.html", {"request": request, **ctx})


# ─── Products management ─────────────────────────────────
@admin_router.get("/products", response_class=HTMLResponse, name="admin.products")
async def admin_products(request: Request, search: Optional[str] = Query(None)):
    if not _require_auth(request):
        return RedirectResponse(url="/auth/login", status_code=302)

    ctx = _admin_context(request, "Quản lý Sản Phẩm", "Products")
    products = get_all_products()
    if search:
        q = search.lower()
        products = [p for p in products if q in p.name.lower()]
    ctx.update({
        "products": products,
        "search": search or "",
    })
    return templates.TemplateResponse("admin/products/index.html", {"request": request, **ctx})


# ─── Categories management ────────────────────────────────
@admin_router.get("/categories", response_class=HTMLResponse, name="admin.categories")
async def admin_categories(request: Request):
    if not _require_auth(request):
        return RedirectResponse(url="/auth/login", status_code=302)

    ctx = _admin_context(request, "Quản lý Danh mục", "Categories")
    ctx["categories"] = get_all_categories()
    return templates.TemplateResponse("admin/categories/index.html", {"request": request, **ctx})


# ─── Orders management ────────────────────────────────────
@admin_router.get("/orders", response_class=HTMLResponse, name="admin.orders")
async def admin_orders(request: Request):
    if not _require_auth(request):
        return RedirectResponse(url="/auth/login", status_code=302)

    ctx = _admin_context(request, "Quản lý Đơn hàng", "Orders")
    ctx["orders"] = get_all_orders()
    return templates.TemplateResponse("admin/orders/index.html", {"request": request, **ctx})


# ─── Accounts management ──────────────────────────────────
@admin_router.get("/accounts", response_class=HTMLResponse, name="admin.accounts")
async def admin_accounts(request: Request):
    if not _require_auth(request):
        return RedirectResponse(url="/auth/login", status_code=302)

    ctx = _admin_context(request, "Quản lý Tài khoản", "Accounts")
    ctx["accounts"] = get_all_accounts()
    return templates.TemplateResponse("admin/accounts/index.html", {"request": request, **ctx})


# ─── Suppliers management ────────────────────────────────
@admin_router.get("/suppliers", response_class=HTMLResponse, name="admin.suppliers")
async def admin_suppliers(request: Request):
    if not _require_auth(request):
        return RedirectResponse(url="/auth/login", status_code=302)

    ctx = _admin_context(request, "Quản lý Nhà cung cấp", "Suppliers")
    ctx["suppliers"] = get_all_suppliers()
    return templates.TemplateResponse("admin/suppliers/index.html", {"request": request, **ctx})
