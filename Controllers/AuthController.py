"""
Auth Controller - Xac thuc nguoi dung
Tuong duong Controllers/AuthController.cs trong ASP.NET Core
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.AuthService import AuthService
from Utilities.auth import require_account, get_current_user
import urllib.parse

router = APIRouter(prefix="/Auth")


@router.get("/Login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    """Trang dang nhap"""
    current_user = get_current_user(request, db)
    return templates.TemplateResponse(
        "Auth/Login.html",
        {
            "request": request,
            "page_title": "Dang nhap",
            "current_user": current_user,
        }
    )


@router.post("/Login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Xu ly dang nhap"""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(username, password)

    if not user:
        error = urllib.parse.quote("Ten dang nhap hoac mat khau khong dung")
        return RedirectResponse(url=f"/Auth/Login?error={error}", status_code=303)

    # Tao token voi role
    token = auth_service.create_access_token(
        user.account_id,
        user.username,
        user.role_name
    )

    # Redirect theo role
    if user.role_name == "Admin":
        redirect_url = "/Admin"
    else:
        redirect_url = "/"

    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return response


@router.get("/Admin", response_class=HTMLResponse)
async def admin_login_page(request: Request, db: Session = Depends(get_db)):
    """Trang dang nhap Admin"""
    current_user = get_current_user(request, db)
    # Neu da dang nhap Admin roi thi chuyen den dashboard
    if current_user and current_user.role_name == "Admin":
        return RedirectResponse(url="/Admin/Dashboard", status_code=303)
    return templates.TemplateResponse(
        "Auth/AdminLogin.html",
        {
            "request": request,
            "page_title": "Dang nhap Quan tri",
            "current_user": current_user,
        }
    )


@router.post("/Admin")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Xu ly dang nhap Admin"""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(username, password)

    if not user:
        error = urllib.parse.quote("Ten dang nhap hoac mat khau khong dung")
        return RedirectResponse(url=f"/Auth/Admin?error={error}", status_code=303)

    # Chi cho phep Admin
    if user.role_name != "Admin":
        error = urllib.parse.quote("Ban khong co quyen truy cap trang nay")
        return RedirectResponse(url=f"/Auth/Admin?error={error}", status_code=303)

    # Tao token
    token = auth_service.create_access_token(
        user.account_id,
        user.username,
        user.role_name
    )

    response = RedirectResponse(url="/Admin/Dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return response


@router.get("/Register", response_class=HTMLResponse)
async def register_page(request: Request, db: Session = Depends(get_db)):
    """Trang dang ky"""
    current_user = get_current_user(request, db)
    return templates.TemplateResponse(
        "Auth/Register.html",
        {
            "request": request,
            "page_title": "Dang ky",
            "current_user": current_user,
        }
    )


@router.post("/Register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(""),
    email: str = Form(""),
    phone: str = Form(""),
    address: str = Form(""),
    role: str = Form("Customer"),
    db: Session = Depends(get_db)
):
    """Xu ly dang ky - khach hang hoac admin"""
    auth_service = AuthService(db)

    try:
        user = auth_service.register_user(
            username, email, password,
            full_name, phone, address, role
        )
    except ValueError as e:
        error = urllib.parse.quote(str(e))
        return RedirectResponse(url=f"/Auth/Register?error={error}", status_code=303)
    except Exception as e:
        error = urllib.parse.quote(str(e))
        return RedirectResponse(url=f"/Auth/Register?error={error}", status_code=303)

    return RedirectResponse(url="/Auth/Login?success=1", status_code=303)


@router.get("/Logout")
async def logout():
    """Dang xuat"""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response


@router.get("/ForgotPassword", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Trang quen mat khau"""
    return templates.TemplateResponse(
        "Auth/ForgotPassword.html",
        {"request": request, "page_title": "Quen mat khau"}
    )


@router.post("/ForgotPassword")
async def forgot_password(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    """Yeu cau dat lai mat khau"""
    auth_service = AuthService(db)
    try:
        token = auth_service.create_reset_token(email)
    except ValueError as exc:
        error = urllib.parse.quote(str(exc))
        return RedirectResponse(url=f"/Auth/ForgotPassword?error={error}", status_code=303)
    success = urllib.parse.quote("Da gui lien ket dat lai mat khau den email cua ban!")
    return RedirectResponse(url=f"/Auth/ForgotPassword?success={success}", status_code=303)


@router.get("/Profile", response_class=HTMLResponse)
async def profile(request: Request, db: Session = Depends(get_db)):
    """Trang thong tin ca nhan"""
    try:
        user = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)
    return templates.TemplateResponse(
        "Auth/Profile.html",
        {"request": request, "page_title": "Thong tin ca nhan", "user": user}
    )


# Templates
templates = None

def set_templates(t):
    global templates
    templates = t
