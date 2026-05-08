"""
URLs cho app faqs.
"""
from django.urls import path
from . import views

app_name = 'faqs'

urlpatterns = [
    # Public URL (Shop)
    path('support/', views.support, name='support'),
    
    # Admin URLs
    path('', views.faq_list, name='faq_list'),
    path('create/', views.faq_create, name='faq_create'),
    path('<int:pk>/edit/', views.faq_update, name='faq_update'),
    path('<int:pk>/delete/', views.faq_delete, name='faq_delete'),
    path('<int:pk>/toggle/', views.faq_toggle_status, name='faq_toggle'),
]
