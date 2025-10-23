# mini_insta/urls.py
# Gracious Ogyiri Asare- gpoa@bu.edu

from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # URL patterns for the mini_insta app
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('show_all_profiles/', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),  
    path('profile/create_post/', CreatePostView.as_view(), name='create_post'),  
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers/', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following/', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/feed/', PostFeedListView.as_view(), name='show_feed'),
    path('profile/search/', SearchView.as_view(), name='profile_search'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'),
    path('logout_confirmation/', TemplateView.as_view(template_name='mini_insta/logged_out.html'), name='logout_confirmation'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]