"""
URL configuration for techshop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.urls')),
    path('accounts/', include('apps.users.urls')),
    path('categories/', include('apps.categories.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
    path('products/', include('apps.products.urls')),
    path('orders/', include('apps.orders.urls')),
    path('cart/', include('apps.cart.urls')),
    path('reports/', include('apps.reports.urls')),
    path('chat/', include('apps.chat.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('faqs/', include('apps.faqs.urls')),
    path('settings/', include('apps.settings.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('shop/', include('apps.shop.urls')),
    path('brands/', include('apps.brands.urls')),
    path('slides/', include('apps.slides.urls')),
    path('reviews/', include('apps.reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
