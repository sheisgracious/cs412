#file: quotes/urls.py

from django.urls import path
from django.conf import settings
from . import views

# Define URL patterns for the quotes app
urlpatterns = [
    path(r'', views.quote, name='main_page'),  # Home page
    path(r'quote/', views.quote, name='quote_page'),  # Random quote page
    path(r'show_all/', views.show_all, name='show_all'),  # Show
    path(r'about/', views.about, name='about'),  # About page
]