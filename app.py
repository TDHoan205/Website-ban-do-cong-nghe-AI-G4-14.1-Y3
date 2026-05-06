"""
Tech Store - Main Application Entry Point
Tương đương Program.cs trong ASP.NET Core

Chạy: uvicorn app:app --reload
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from Data.database import init_db, get_connection_info
from Controllers import (
    HomeController,
    ProductsController,
    CartController,
    AuthController,
    ChatController,
    AccountsController,
    CategoriesController,
    SuppliersController,
    EmployeesController,
    InventoryController,
    OrdersController,
    OrderItemsController,
    ReceiptShipmentsController,
    CartItemsController,
    SeedController,
    ShopController,
    StatisticsController,
)

# =====================================================================
# FastAPI Application
# =====================================================================
app = FastAPI(
    title="Tech Store - Website bán đồ công nghệ",
    description="Website thương mại điện tử với AI Chatbot",
    version="1.0.0",
    debug=True,
)

# =====================================================================
# Static Files (tương đương app.UseStaticFiles() trong .NET)
# =====================================================================
wwwroot_path = os.path.join(os.path.dirname(__file__), "wwwroot")
os.makedirs(wwwroot_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=wwwroot_path), name="static")

# =====================================================================
# Templates Configuration (tương đương AddRazorPages() trong .NET)
# =====================================================================
views_path = os.path.join(os.path.dirname(__file__), "Views")
templates = Jinja2Templates(directory=views_path)

# Global variables cho tất cả templates
templates.env.globals.update({
    "app_name": "Tech Store",
    "app_version": "1.0.0",
    "current_year": 2024,
})

# =====================================================================
# Register Controllers với templates
# =====================================================================
HomeController.set_templates(templates)
ProductsController.set_templates(templates)
CartController.set_templates(templates)
AuthController.set_templates(templates)
ChatController.set_templates(templates)

# =====================================================================
# Include Routers
# =====================================================================
app.include_router(HomeController.router)
app.include_router(ProductsController.router)
app.include_router(CartController.router)
app.include_router(AuthController.router)
app.include_router(ChatController.router)
app.include_router(AccountsController.router)
app.include_router(CategoriesController.router)
app.include_router(SuppliersController.router)
app.include_router(EmployeesController.router)
app.include_router(InventoryController.router)
app.include_router(OrdersController.router)
app.include_router(OrderItemsController.router)
app.include_router(ReceiptShipmentsController.router)
app.include_router(CartItemsController.router)
app.include_router(SeedController.router)
app.include_router(ShopController.router)
app.include_router(StatisticsController.router)


# =====================================================================
# Startup & Shutdown Events
# =====================================================================

@app.on_event("startup")
async def startup():
    """Khoi dong ung dung"""
    db_info = get_connection_info()
    print(f"""
+--------------------------------------------------------------+
|              TECH STORE APPLICATION STARTED                   |
+--------------------------------------------------------------+
|  Database : {db_info['database']:<46} |
|  Server   : {db_info['server']:<46} |
|  Auth     : {db_info['auth_mode']:<46} |
|  URL      : http://localhost:8000                            |
|  Docs     : http://localhost:8000/docs                       |
+--------------------------------------------------------------+
    """)


@app.on_event("shutdown")
async def shutdown():
    """Tắt ứng dụng"""
    print("\nTech Store Application Shutdown")


# =====================================================================
# Error Handlers
# =====================================================================

@app.exception_handler(404)
async def not_found(request: Request, exc):
    """Xử lý lỗi 404"""
    return templates.TemplateResponse(
        "Shared/error.html",
        {
            "request": request,
            "error_code": 404,
            "error_message": "Trang không tìm thấy"
        },
        status_code=404
    )


@app.exception_handler(500)
async def server_error(request: Request, exc):
    """Xử lý lỗi 500"""
    return templates.TemplateResponse(
        "Shared/error.html",
        {
            "request": request,
            "error_code": 500,
            "error_message": "Lỗi server"
        },
        status_code=500
    )


# =====================================================================
# Development Entry Point
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
