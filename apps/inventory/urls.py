"""
URLs cho app inventory.
"""
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('adjust/', views.inventory_adjustment, name='inventory_adjustment'),
    path('movements/', views.inventory_movements, name='inventory_movements'),
    path('alerts/', views.low_stock_alerts, name='low_stock_alerts'),
]
