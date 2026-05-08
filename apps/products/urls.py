"""
URLs cho app products.
"""
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product CRUD
    path('', views.product_list, name='product_list'),
    path('bulk/', views.product_bulk, name='product_bulk'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/edit/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('<int:pk>/toggle-status/', views.product_toggle_status, name='product_toggle_status'),

    # Product Variants
    path('<int:product_pk>/variants/', views.variant_list, name='variant_list'),
    path('<int:product_pk>/variants/create/', views.variant_create, name='variant_create'),
    path('<int:product_pk>/variants/<int:variant_pk>/edit/', views.variant_update, name='variant_update'),
    path('<int:product_pk>/variants/<int:variant_pk>/delete/', views.variant_delete, name='variant_delete'),

    # Product Images
    path('<int:product_pk>/images/', views.image_list, name='image_list'),
    path('<int:product_pk>/images/create/', views.image_create, name='image_create'),
    path('<int:product_pk>/images/<int:image_pk>/delete/', views.image_delete, name='image_delete'),
]
