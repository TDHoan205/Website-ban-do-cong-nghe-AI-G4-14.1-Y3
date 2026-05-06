"""
Auth Controller - Xác thực người dùng
Tương đương Controllers/AuthController.cs trong ASP.NET Core
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Services.AuthService import AuthService
from Utilities.auth import require_account

router = APIRouter(prefix="/Auth")




@router.get("/Login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Trang đăng nhập"""
    return templates.TemplateResponse(
        "Auth/Login.html",
        {"request": request, "page_title": "Đăng nhập"}
    )


@router.post("/Login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Xử lý đăng nhập"""
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(username, password)

    if not user:
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc mật khẩu không đúng")

    token = auth_service.create_access_token(user.account_id, user.username, user.role_name)
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )
    return response


@router.get("/Register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Trang đăng ký"""
    return templates.TemplateResponse(
        "Auth/Register.html",
        {"request": request, "page_title": "Đăng ký"}
    )


@router.post("/Register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    full_name: str = Form(""),
    phone: str = Form(""),
    db: Session = Depends(get_db)
):
    """Xử lý đăng ký"""
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Mật khẩu không khớp")

    auth_service = AuthService(db)

    try:
        user = auth_service.register_user(username, email, password, full_name, phone)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RedirectResponse(url="/Auth/Login", status_code=303)


@router.get("/Logout")
async def logout():
    """Đăng xuất"""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response


@router.post("/ForgotPassword")
async def forgot_password(
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    """Yeu cau dat lai mat khau"""
    auth_service = AuthService(db)
    try:
        token = auth_service.create_reset_token(email)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return JSONResponse({"success": True, "reset_token": token})


@router.post("/ResetPassword")
async def reset_password(
    token: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Dat lai mat khau"""
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Mật khẩu không khớp")
    auth_service = AuthService(db)
    ok = auth_service.reset_password(token, new_password)
    if not ok:
        raise HTTPException(status_code=400, detail="Token không hợp lệ hoặc đã hết hạn")
    return JSONResponse({"success": True})


@router.get("/Profile", response_class=HTMLResponse)
async def profile(request: Request, db: Session = Depends(get_db)):
    """Trang thông tin cá nhân"""
    try:
        user = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)
    return templates.TemplateResponse(
        "Auth/Profile.html",
        {"request": request, "page_title": "Thông tin cá nhân", "user": user}
    )


# Templates
templates = None

def set_templates(t):
    global templates
    templates = t
