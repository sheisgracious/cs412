from django.db import models

# Create your models here.
class Article(models.Model):
    '''Model representing a blog article.'''

    # define data fields of the Article model
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True) #set the published date automatically
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''String for representing the Model object.'''
        return f'{self.title} by {self.author}'