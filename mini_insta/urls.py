# mini_insta/urls.py
from django.urls import path
from .views import ProfileListView  

urlpatterns = [
    # URL patterns for the mini_insta app
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('show_all_profiles/', ProfileListView.as_view(), name='show_all_profiles'),
]