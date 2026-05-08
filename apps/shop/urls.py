"""
URLs cho app shop.
"""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Trang chủ
    path('', views.shop_home, name='home'),
    
    # Danh sách sản phẩm
    path('products/', views.product_list, name='product_list'),
    
    # Chi tiết sản phẩm
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Giỏ hàng
    path('cart/', views.cart_view, name='cart'),
    
    # Thanh toán
    path('checkout/', views.checkout_view, name='checkout'),
    
    # API giỏ hàng
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/count/', views.get_cart_count, name='cart_count'),
    
    # Tìm kiếm gợi ý
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
]
