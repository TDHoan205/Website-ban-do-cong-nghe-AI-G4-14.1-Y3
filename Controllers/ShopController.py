"""
Shop Controller - Alias cho danh sach san pham
Tuong duong Controllers/ShopController.cs trong C#
"""
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/Shop")


@router.get("")
def index():
    return RedirectResponse(url="/Products", status_code=307)
