"""
URLs cho app wishlist.
"""
from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add/', views.add_to_wishlist, name='add'),
    path('remove/', views.remove_from_wishlist, name='remove'),
    path('count/', views.get_wishlist_count, name='count'),
    path('recent/', views.get_recently_viewed, name='recent'),
    path('track/', views.track_viewed, name='track'),
]
