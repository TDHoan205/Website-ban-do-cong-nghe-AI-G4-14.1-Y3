"""
URLs cho app shop.
"""
from django.urls import path
from . import views
from apps.cart.views import cart_view, checkout_view, add_to_cart_api, update_cart_api, remove_cart_api, get_cart_count_api

app_name = 'shop'

urlpatterns = [
    # Trang chu
    path('', views.shop_home, name='home'),

    # Danh sach san pham
    path('products/', views.product_list, name='product_list'),

    # Chi tiet san pham
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),

    # Gio hang (delegate to cart app)
    path('cart/', cart_view, name='cart'),

    # Thanh toan (delegate to cart app)
    path('checkout/', checkout_view, name='checkout'),

    # API gio hang (delegate to cart app)
    path('cart/add/', add_to_cart_api, name='add_to_cart'),
    path('cart/update/', update_cart_api, name='update_cart'),
    path('cart/remove/', remove_cart_api, name='remove_from_cart'),
    path('cart/count/', get_cart_count_api, name='cart_count'),

    # Tim kiem goi y
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),

    # Chinh sach bao mat (public)
    path('privacy/', views.privacy_policy, name='privacy'),
]
