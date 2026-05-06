"""
FastAPI main application - Webstore with real SQL Server database.
Entry point: run `python -m uvicorn flask_app.main:app --reload`

Prerequisites:
  1. Install dependencies: pip install -r flask_app/requirements.txt
  2. Update database credentials in flask_app/database.py
  3. Run the schema: SQL/schema.sql
  4. Seed data: python flask_app/seed_data.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from .database import SessionLocal
from .models import Account
from .app_config import templates  # Shared templates with custom filters registered

# ── App setup ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="Webstore - Hệ thống bán hàng trực tuyến",
    description="Hệ thống bán hàng trực tuyến với FastAPI + SQL Server",
    version="2.0.0",
)

# ── Static files ───────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ── Root redirect ────────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/shop/", status_code=302)

# ── Register routers ─────────────────────────────────────────────────────
from .routers import auth_router, admin_router, api_router, web_router

app.include_router(web_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(api_router)

# ── 404 handler ─────────────────────────────────────────────────────────
@app.exception_handler(404)
async def page_not_found(request: Request, exc):
    from datetime import datetime
    ctx = {
        "request": request,
        "title": "Không tìm thấy trang",
        "current_user": None,
        "is_admin": False,
        "is_employee": False,
        "is_authenticated": False,
        "cart_count": 0,
        "app_name": "TechStore",
        "current_year": datetime.now().year,
    }
    return templates.TemplateResponse("errors/404.html", ctx, status_code=404)
