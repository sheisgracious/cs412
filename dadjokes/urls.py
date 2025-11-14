# dadjokes/urls.py
# Gracious Ogyiri Asare- gpoa@bu.edu

from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # URL patterns for the dadjokes app
    path('', RandomJokeView.as_view(), name='show_all_jokes'),
    path('random', RandomJokeView.as_view(), name='random_joke'),
    path('jokes/', ShowAllJokes.as_view(), name='show_all_jokes'),
    path('joke/<int:pk>/', JokeDetailView.as_view(), name='show_joke'),
    path('pictures/', ShowAllPictures.as_view(), name='show_all_pictures'),
    path('picture/<int:pk>/', PictureDetailView.as_view(), name='show_picture'),

    ##API Views:
    path(r'api/', RandomJokeAPIView.as_view(), name='random_joke_api'),
    path(r'api/random', RandomJokeAPIView.as_view(), name='random_joke_api'),
    path(r'api/jokes/', JokeListAPIView.as_view(), name='joke_list_api'),
    path(r'api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='joke_pk_api'),
    path(r'api/pictures/', PictureListAPIView.as_view(), name='picture_list_api'),
    path(r'api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='picture_pk_api'), 
    path(r'api/random_picture', RandomPictureAPIView.as_view(), name='random_picture_api'),
]