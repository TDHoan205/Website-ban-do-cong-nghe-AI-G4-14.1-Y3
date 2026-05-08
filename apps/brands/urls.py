"""
URLs cho app brands.
"""
from django.urls import path
from . import views

app_name = 'brands'

urlpatterns = [
    path('', views.brand_list, name='brand_list'),
    path('create/', views.brand_create, name='brand_create'),
    path('<int:pk>/edit/', views.brand_update, name='brand_update'),
    path('<int:pk>/delete/', views.brand_delete, name='brand_delete'),
    path('<int:pk>/toggle-status/', views.brand_toggle_status, name='brand_toggle_status'),
]
