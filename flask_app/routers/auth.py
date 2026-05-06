"""
Auth routes – login, register, logout.
"""
from fastapi import APIRouter, Request, Form, Cookie, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional

from ..app_config import templates
from ..services import authenticate, get_or_create_session, set_session_user, logout_session, get_session

auth_router = APIRouter(prefix="", tags=["Auth"])


@auth_router.get("/auth/login", response_class=HTMLResponse, name="auth.login")
async def login_page(request: Request, return_url: Optional[str] = None):
    session_id = request.cookies.get("session_id", "")
    session = get_session(session_id) if session_id else {}
    if session.get("username"):
        return RedirectResponse(url="/shop", status_code=302)

    ctx = {"title": "Đăng nhập", "return_url": return_url or ""}
    return templates.TemplateResponse("auth/login.html", {"request": request, **ctx})


@auth_router.post("/auth/login", name="auth.login_post")
async def login_submit(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    return_url: Optional[str] = Form(None),
):
    account = authenticate(username, password)
    if not account:
        ctx = {"title": "Đăng nhập", "error": "Tên đăng nhập hoặc mật khẩu không đúng.",
               "return_url": return_url or ""}
        return templates.TemplateResponse("auth/login.html", {"request": request, **ctx})

    session_id, _ = get_or_create_session(request.cookies.get("session_id"))
    set_session_user(session_id, account.account_id, account.username, account.role)

    redirect_url = return_url or (
        "/admin" if account.role == "Admin" else "/shop"
    )
    resp = RedirectResponse(url=redirect_url, status_code=302)
    resp.set_cookie("session_id", session_id, httponly=True, samesite="lax", max_age=86400)
    return resp


@auth_router.get("/auth/register", response_class=HTMLResponse, name="auth.register")
async def register_page(request: Request):
    ctx = {"title": "Đăng ký"}
    return templates.TemplateResponse("auth/register.html", {"request": request, **ctx})


@auth_router.post("/auth/register", name="auth.register_post")
async def register_submit(
    request: Request,
    response: Response,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
):
    ctx = {"title": "Đăng ký", "success": "Đăng ký thành công! Vui lòng đăng nhập."}
    return templates.TemplateResponse("auth/register.html", {"request": request, **ctx})


@auth_router.get("/auth/logout", name="auth.logout")
async def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        logout_session(session_id)
    resp = RedirectResponse(url="/", status_code=302)
    resp.delete_cookie("session_id")
    return resp


@auth_router.get("/auth/forgot-password", response_class=HTMLResponse, name="auth.forgot_password")
async def forgot_password(request: Request):
    ctx = {"title": "Quên mật khẩu"}
    return templates.TemplateResponse("auth/forgot_password.html", {"request": request, **ctx})


@auth_router.post("/auth/forgot-password", name="auth.forgot_password_post")
async def forgot_password_submit(request: Request):
    ctx = {"title": "Quên mật khẩu",
           "success": "Liên kết đặt lại mật khẩu đã được gửi đến email của bạn."}
    return templates.TemplateResponse("auth/forgot_password.html", {"request": request, **ctx})


@auth_router.get("/auth/reset-password", response_class=HTMLResponse, name="auth.reset_password")
async def reset_password(request: Request):
    ctx = {"title": "Đặt lại mật khẩu"}
    return templates.TemplateResponse("auth/reset_password.html", {"request": request, **ctx})
