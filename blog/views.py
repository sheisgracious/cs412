from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.
class ShowAllView(ListView):
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #plural name similar to model name- contains many instances of the model
    ordering = ['-published']  # Order by published date descending

class ArticleView(DetailView):
    '''Display a single article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'  # contains one instance of the model

class RandomArticleView(DetailView):
    '''Display a random article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article' 

    # methods
    def get_object(self, queryset=None):
        '''return one instance of the Article object'''
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article