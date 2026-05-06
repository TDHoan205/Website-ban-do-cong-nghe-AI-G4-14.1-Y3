"""
Auth router – login, register, logout using real SQL Server database.
"""
from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..services import AuthService
from ..session import login, logout, get_session_token, get_session, is_authenticated
from ..models import Account

from ..app_config import templates


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# ── GET /auth/login ─────────────────────────────────────────────
@auth_router.get("/login", response_class=HTMLResponse, name="auth.login")
async def login_page(request: Request, return_url: Optional[str] = None):
    if is_authenticated(request):
        return RedirectResponse(url=return_url or "/shop/", status_code=302)

    ctx = {
        "request": request,
        "title": "Đăng nhập",
        "return_url": return_url or "",
        "error": None,
    }
    return templates.TemplateResponse("auth/login.html", ctx)


# ── POST /auth/login ─────────────────────────────────────────────
@auth_router.post("/login", name="auth.login_post")
async def login_submit(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    return_url: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    auth_svc = AuthService(db)
    account = auth_svc.authenticate(username, password)

    if not account:
        ctx = {
            "request": request,
            "title": "Đăng nhập",
            "return_url": return_url or "",
            "error": "Tên đăng nhập hoặc mật khẩu không đúng.",
        }
        return templates.TemplateResponse("auth/login.html", ctx)

    # Create session
    guest_uuid = None  # TODO: link guest cart to account on login
    login(response, account, guest_uuid)

    redirect_url = return_url or "/shop/"
    return RedirectResponse(url=redirect_url, status_code=302)


# ── GET /auth/logout ─────────────────────────────────────────────
@auth_router.get("/logout", name="auth.logout")
async def logout_get(request: Request, response: Response):
    logout(response, request)
    return RedirectResponse(url="/shop/", status_code=302)


# ── POST /auth/logout ─────────────────────────────────────────────
@auth_router.post("/logout", name="auth.logout_post")
async def logout_post(request: Request, response: Response):
    logout(response, request)
    return RedirectResponse(url="/shop/", status_code=302)


# ── GET /auth/register ─────────────────────────────────────────────
@auth_router.get("/register", response_class=HTMLResponse, name="auth.register")
async def register_page(request: Request):
    if is_authenticated(request):
        return RedirectResponse(url="/shop/", status_code=302)

    ctx = {
        "request": request,
        "title": "Đăng ký",
        "error": None,
        "success": None,
    }
    return templates.TemplateResponse("auth/register.html", ctx)


# ── POST /auth/register ─────────────────────────────────────────────
@auth_router.post("/register", name="auth.register_post")
async def register_submit(
    request: Request,
    response: Response,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    db: Session = Depends(get_db),
):
    auth_svc = AuthService(db)

    # Check if username already exists
    if auth_svc.get_account_by_username(username):
        ctx = {
            "request": request,
            "title": "Đăng ký",
            "error": "Tên đăng nhập đã được sử dụng.",
            "success": None,
        }
        return templates.TemplateResponse("auth/register.html", ctx)

    # Check if email already exists
    if auth_svc.get_account_by_email(email):
        ctx = {
            "request": request,
            "title": "Đăng ký",
            "error": "Email đã được sử dụng.",
            "success": None,
        }
        return templates.TemplateResponse("auth/register.html", ctx)

    # Create account
    account = auth_svc.create_account(
        username=username,
        email=email,
        password=password,
        full_name=full_name,
        role_name="Customer",
    )

    # Auto-login
    login(response, account)

    return RedirectResponse(url="/shop/", status_code=302)
