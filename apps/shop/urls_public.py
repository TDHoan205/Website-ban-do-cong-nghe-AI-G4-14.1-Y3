"""
URLs công khai cho shop với prefix /shop/
"""
from django.urls import path, include
from . import views
from apps.cart.views import cart_view, checkout_view, add_to_cart_api, update_cart_api, remove_cart_api, get_cart_count_api

app_name = 'shop'

urlpatterns = [
    # Trang chu - /shop/
    path('', views.shop_home, name='home'),

    # Danh sach san pham - /shop/products/
    path('products/', views.product_list, name='product_list'),

    # Chi tiet san pham - /shop/products/<id>/
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),

    # Gio hang - /shop/cart/
    path('cart/', cart_view, name='cart'),

    # Thanh toan - /shop/checkout/
    path('checkout/', checkout_view, name='checkout'),

    # API gio hang - /shop/cart/add/, /shop/cart/update/, /shop/cart/remove/, /shop/cart/count/
    path('cart/add/', add_to_cart_api, name='add_to_cart'),
    path('cart/update/', update_cart_api, name='update_cart'),
    path('cart/remove/', remove_cart_api, name='remove_from_cart'),
    path('cart/count/', get_cart_count_api, name='cart_count'),

    # Tim kiem goi y - /shop/search/suggestions/
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),

    # Chinh sach bao mat - /shop/privacy/
    path('privacy/', views.privacy_policy, name='privacy'),

    # Dieu khoan su dung - /shop/terms/
    path('terms/', views.terms_of_service, name='terms'),
]
