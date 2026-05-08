"""
URLs cho app orders.
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:pk>/edit/', views.order_update, name='order_update'),
    path('<int:pk>/update-status/', views.order_update_status, name='order_update_status'),
    path('<int:pk>/cancel/', views.order_cancel, name='order_cancel'),
    path('statistics/', views.order_statistics, name='order_statistics'),
]
