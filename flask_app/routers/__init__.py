from .shop import shop_router
from .auth import auth_router
from .admin import admin_router
from .api import api_router

__all__ = ["shop_router", "auth_router", "admin_router", "api_router"]
