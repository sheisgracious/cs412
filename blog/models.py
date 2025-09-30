from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        '''Returns the url to access a detail record for this article.'''
        return reverse('article', kwargs={'pk': self.pk})
    def get_all_comments(self):
        '''Return a QuerySet of comments about this article.'''
        comments = Comment.objects.filter(article=self)
        return comments
    

class Comment(models.Model):
    '''Encapsulate the idea of a comment on an article.'''

    # data attributes
    article = models.ForeignKey(Article, on_delete=models.CASCADE) #foreign key to Article model
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True) 

    def __str__(self):
        '''String for representing the Model object.'''
        return f'{self.text}'
    

