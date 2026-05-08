"""
URLs cho app chat.
"""
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('analytics/', views.chat_analytics, name='chat_analytics'),
    path('start/', views.chat_start, name='chat_start'),
    path('ai-logs/', views.ai_logs, name='ai_logs'),
    path('ai-status/', views.ai_status, name='ai_status'),
    # API endpoints
    path('api/send/', views.api_send_message, name='api_send'),
    path('api/history/<uuid:session_id>/', views.api_get_history, name='api_history'),
    path('api/new-messages/<uuid:session_id>/', views.api_new_messages, name='api_new_messages'),
    path('api/escalate/', views.api_escalate, name='api_escalate'),
    # Admin views
    path('<uuid:session_id>/', views.chat_detail, name='chat_detail'),
    path('<uuid:session_id>/send/', views.chat_send_message, name='chat_send_message'),
    path('<uuid:session_id>/assign/', views.chat_assign, name='chat_assign'),
    path('<uuid:session_id>/close/', views.chat_close, name='chat_close'),
]
