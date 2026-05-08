"""
URLs cho app inventory.
"""
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('adjust/', views.inventory_adjustment, name='inventory_adjustment'),
]
