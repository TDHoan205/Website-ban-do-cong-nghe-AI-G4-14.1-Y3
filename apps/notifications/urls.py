"""
URLs cho app notifications.
"""
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('create/', views.notification_create_all, name='notification_create'),
    path('<int:pk>/read/', views.notification_mark_read, name='notification_read'),
    path('read-all/', views.notification_mark_all_read, name='notification_read_all'),
    path('<int:pk>/delete/', views.notification_delete, name='notification_delete'),
    path('delete-all/', views.notification_delete_all, name='notification_delete_all'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
]
