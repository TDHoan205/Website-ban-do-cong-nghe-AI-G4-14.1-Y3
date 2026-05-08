"""
URLs cho app dashboard.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('reports/', views.reports, name='reports'),
]
