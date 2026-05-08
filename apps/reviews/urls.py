"""
URLs cho app reviews.
"""
from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('<int:pk>/edit/', views.review_update, name='review_update'),
    path('<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:pk>/toggle-approval/', views.review_toggle_approval, name='review_toggle_approval'),
    path('approve-all/', views.review_approve_all, name='review_approve_all'),
]
