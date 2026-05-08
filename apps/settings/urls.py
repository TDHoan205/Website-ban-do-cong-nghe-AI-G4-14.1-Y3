"""
URLs cho app settings.
"""
from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_list, name='settings_list'),
    path('create/', views.setting_create, name='setting_create'),
    path('<int:pk>/', views.setting_update, name='setting_update'),
    path('<int:pk>/delete/', views.setting_delete, name='setting_delete'),
    path('maintenance/', views.maintenance_update, name='maintenance'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
]
