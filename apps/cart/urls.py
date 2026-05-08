"""
URLs cho app cart.
"""
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Public URLs
    path('checkout/', views.checkout_view, name='checkout'),
    path('add-to-cart/', views.add_to_cart_api, name='add_to_cart_api'),
    
    # Admin URLs
    path('admin/', views.cart_list, name='cart_list'),
    path('admin/<int:account_pk>/', views.cart_detail, name='cart_detail'),
    path('admin/add/', views.cart_add, name='cart_add'),
    path('admin/<int:pk>/update/', views.cart_update, name='cart_update'),
    path('admin/<int:pk>/remove/', views.cart_remove, name='cart_remove'),
]
