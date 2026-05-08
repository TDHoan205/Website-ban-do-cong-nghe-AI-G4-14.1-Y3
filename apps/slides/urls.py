"""
URLs cho app slides.
"""
from django.urls import path
from . import views

app_name = 'slides'

urlpatterns = [
    path('', views.slide_list, name='slide_list'),
    path('create/', views.slide_create, name='slide_create'),
    path('<int:pk>/edit/', views.slide_update, name='slide_update'),
    path('<int:pk>/delete/', views.slide_delete, name='slide_delete'),
    path('<int:pk>/toggle-status/', views.slide_toggle_status, name='slide_toggle_status'),
]
