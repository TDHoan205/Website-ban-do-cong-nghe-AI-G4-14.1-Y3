"""
FastAPI main application – Webstore Flask MVC demo.
Entry point: run `python run.py` from the project root.
"""
import os
import sys

# Add project root to path so 'flask_app' is importable as a package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from flask_app.app_config import templates, STATIC_DIR

# ─── App setup ───────────────────────────────────────────
app = FastAPI(
    title="Webstore - Hệ thống bán hàng trực tuyến",
    description="Demo Flask/ASP.NET MVC conversion project",
    version="1.0.0",
)

# ─── Static files ────────────────────────────────────────
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ─── Register routers ────────────────────────────────────
from flask_app.routers import shop_router, auth_router, admin_router, api_router

app.include_router(shop_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(api_router)


# ─── Root redirect ───────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/shop", status_code=302)


# ─── 404 handler ───────────────────────────────────────
@app.exception_handler(404)
async def page_not_found(request: Request, exc):
    return templates.TemplateResponse(
        "errors/404.html",
        {"request": request, "title": "Không tìm thấy trang"},
    )
