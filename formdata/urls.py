# formdata/urls.py
from django.urls import path
from django.conf import settings
from . import views

# URL patterns for this app
urlpatterns = [
    path('', views.show_form, name='show_form'), #New
    path('submit/', views.submit, name='submit'), #New
]