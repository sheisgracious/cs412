# restaurant/urls.py
from django.urls import path
from django.conf import settings
from . import views

# URL patterns for this app
urlpatterns = [
path('', views.main, name='main'), 
path('main/', views.main, name='main'),
path('order/', views.order, name='order'), 
path('submit_order/', views.submit_order, name='submit_order')
]