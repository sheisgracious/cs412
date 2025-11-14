# dadjokes/models.py
# Gracious Ogyiri Asare- gpoa@bu.edu

# define models for the dadjokes app
from django.db import models

# Create your models here.
class Joke(models.Model):
    '''Model representing a joke.'''

    # define data fields of the Joke model
    joke_text = models.TextField(blank=False)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''String represention of the model object'''
        return f'Joke: {self.joke_text} by {self.contributor} at {self.timestamp}'
    
class Picture(models.Model):
    '''model representing a picture connected to the joke'''

    # define data fields of the Picture model
    image_url = models.URLField(blank=True)
    contributor = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''String represention of the model object'''
        return f'image info: {self.image_url} by {self.contributor} at {self.timestamp}'



