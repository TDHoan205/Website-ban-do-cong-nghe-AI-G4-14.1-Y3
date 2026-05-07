"""
URL configuration for techshop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    path('auth/', include('apps.auth.urls', namespace='auth')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('categories/', include('apps.products.urls', namespace='categories')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('accounts/', include('apps.users.urls', namespace='accounts')),
    path('inventory/', include('apps.inventory.urls', namespace='inventory')),
    path('suppliers/', include('apps.products.urls', namespace='suppliers')),
    path('shop/', include('apps.shop.urls', namespace='shop')),
    path('chat/', include('apps.chat.urls', namespace='chat')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
