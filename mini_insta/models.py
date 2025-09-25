# mini_insta/models.py
# define data models for the mini_insta app
from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Model representing a user profile.'''

    # define data fields of the Profile model
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True) #set the joined date automatically
    
    def __str__(self):
        '''String for representing the Model object.'''
        return f'{self.username} is displayed as {self.display_name} and has bio: {self.bio_text}'