"""
URLs cho app reports.
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.revenue_report, name='revenue_report'),
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/products/', views.export_products_csv, name='export_products'),
    path('export/orders/', views.export_orders_csv, name='export_orders'),
    path('export/customers/', views.export_customers_csv, name='export_customers'),
]
