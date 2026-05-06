"""
Shared FastAPI application configuration.
Avoids circular imports between main.py and routers.
"""
from fastapi.templating import Jinja2Templates
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Templates – registered once here, shared everywhere
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ─── url_for helper for Jinja2 (FastAPI-compatible) ────────────────────
def _static_url(path: str) -> str:
    """Return the static file URL, e.g. url_for('static', path='images/logo.png')"""
    return f"/static/{path.lstrip('/')}"


def _url_for(name: str, **kwargs) -> str:
    """
    Flask-compatible url_for for templates.
    Supports:
      url_for('static', path='...') -> /static/...
      url_for('shop.home') -> /shop/
    """
    if name == "static":
        return _static_url(kwargs.get("path", ""))
    if name == "shop.home":
        return "/shop/"
    if name == "shop.products":
        return "/shop/products"
    if name == "shop.cart":
        return "/shop/cart"
    # Fallback
    return "/"

# ─── Custom Jinja2 filters ───────────────────────────────
def format_vnd(amount: float) -> str:
    return f"{amount:,.0f} ₫".replace(",", ".")


def format_currency(amount: float) -> str:
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:,.#}B ₫"
    if amount >= 1_000_000:
        return f"{amount / 1_000_000:,.#}M ₫"
    if amount >= 1_000:
        return f"{amount / 1_000:,.#}K ₫"
    return f"{amount:,.0f} ₫"


def get_category_icon(name: str) -> str:
    if not name:
        return "cube"
    n = name.lower()
    if any(k in n for k in ["điện thoại", "dien thoai", "phone", "iphone", "samsung", "xiaomi"]):
        return "mobile-alt"
    if any(k in n for k in ["laptop", "máy tính", "may tinh", "macbook", "dell", "hp", "asus"]):
        return "laptop"
    if any(k in n for k in ["tablet", "ipad"]):
        return "tablet-alt"
    if any(k in n for k in ["âm thanh", "am thanh", "tai nghe", "headphone", "airpod"]):
        return "headphones-alt"
    if any(k in n for k in ["đồng hồ", "dong ho", "watch", "smartwatch"]):
        return "clock"
    if any(k in n for k in ["phụ kiện", "phu kien", "accessory", "sạc", "sac", "cable"]):
        return "plug"
    if any(k in n for k in ["camera", "webcam"]):
        return "camera"
    if any(k in n for k in ["game", "console"]):
        return "gamepad"
    if any(k in n for k in ["bàn phím", "ban phim", "keyboard"]):
        return "keyboard"
    if any(k in n for k in ["chuột", "chuot", "mouse"]):
        return "mouse"
    return "cube"


def get_status_badge(status: str) -> str:
    return {
        "Completed": "bg-success-soft",
        "New": "bg-primary-soft",
        "Pending": "bg-warning-soft",
        "Canceled": "bg-danger-soft",
        "Processing": "bg-warning-soft",
    }.get(status, "bg-light-soft text-dark")


templates.env.filters["format_vnd"] = format_vnd
templates.env.filters["format_currency"] = format_currency
templates.env.filters["get_category_icon"] = get_category_icon
templates.env.filters["get_status_badge"] = get_status_badge
templates.env.globals["url_for"] = _url_for
templates.env.globals["static_url"] = _static_url
