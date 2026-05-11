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
    path('<int:pk>/payment-status/', views.order_update_payment_status, name='order_update_payment_status'),
    path('<int:pk>/admin-notes/', views.order_update_admin_notes, name='order_update_admin_notes'),
    path('<int:pk>/confirm-payment/', views.order_confirm_payment, name='order_confirm_payment'),
    path('<int:pk>/reject-payment/', views.order_reject_payment, name='order_reject_payment'),
    path('statistics/', views.order_statistics, name='order_statistics'),
    # Customer-facing
    path('history/', views.order_history, name='order_history'),
    path('tracking/', views.order_tracking, name='order_tracking'),
]
