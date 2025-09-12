#file: hw/urls.py

from django.urls import path
from django.conf import settings
from . import views

# Define URL patterns for the hw app
urlpatterns = [
    # path(r'', views.home, name='home'),  # Home page
    path(r'', views.home_page, name='home_page'),  # Home page
    path(r'about/', views.about, name='about_page'),  # About page
]