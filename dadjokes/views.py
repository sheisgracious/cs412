# dadjokes/views.py
# Gracious Ogyiri Asare- gpoa@bu.edu

from django.shortcuts import render
import random
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# Create your views here.
class JokeDetailView(DetailView):
    '''Display single joke.'''
    model = Joke
    template_name = 'dadjokes/joke.html'
    context_object_name = 'joke'

class PictureDetailView(DetailView):
    '''Display single joke.'''
    model = Picture
    template_name = 'dadjokes/picture.html'
    context_object_name = 'picture'

class RandomJokeView(DetailView):
    '''display a random joke'''
    model = Joke
    template_name = 'dadjokes/random.html'
    context_object_name = 'joke'

    # methods
    def get_object(self, queryset=None):
        '''return a random Joke instance'''
        jokes = list(Joke.objects.all())
        return random.choice(jokes)

    def get_context_data(self, **kwargs):
        '''add the related pictures to context'''
        context = super().get_context_data(**kwargs)
        joke = context.get('joke')
        pictures = Picture.objects.filter(contributor=joke.contributor) if joke else Picture.objects.none()
        context['pictures'] = pictures
        context['picture'] = pictures.first() if pictures.exists() else None
        return context

        
class ShowAllJokes(ListView):
    '''display all jokes'''
    model = Joke
    template_name = "dadjokes/all_jokes.html"
    context_object_name = 'jokes'
    ordering = ['-timestamp']

class ShowAllPictures(ListView):
    '''display all pictures'''
    model = Picture
    template_name = "dadjokes/all_pictures.html"
    context_object_name = 'pictures'
    ordering = ['-timestamp']

############################################################################################################
#Rest API Views
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''An API view to return a single joke by pk.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''An API view to return a single picture by pk.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class JokeListAPIView(generics.ListCreateAPIView):
    '''An API view to return a list of all jokes and create a new joke.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListCreateAPIView):
    '''An API view to return a list of all pictures and create a new picture.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomJokeAPIView(generics.RetrieveAPIView):
    '''API to return a random joke'''
    serializer_class = JokeSerializer

    def get_object(self):
        jokes = list(Joke.objects.all())
        return random.choice(jokes) if jokes else None
    
class RandomPictureAPIView(generics.RetrieveAPIView):
    '''API to return a random picture'''
    serializer_class = PictureSerializer

    def get_object(self):
        pictures = list(Picture.objects.all())
        return random.choice(pictures) if pictures else None