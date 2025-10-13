from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
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
    
class CreateArticleView(CreateView):
    '''Create a new article.
    1. Display a HTML form to the user (GET)
    2. Process the form submission and store the new Article object (POST)
    '''
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def form_valid(self, form):
        '''handles the form submission and saves the new article to the database.'''

        print(f'CreateArtleView.form_valid(): {form.cleaned_data}') #debug
        return super().form_valid(form)

class CreateCommentView(CreateView):
    '''Create a new comment for an article.
    '''
    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'

    def get_success_url(self):
        '''provide a URL to redirect to after the form is successfully processed.'''
        pk = self.kwargs['pk']  
        # call reverse to get the URL for the article detail view
        return reverse('article', kwargs={'pk': pk})
    
    def get_context_data(self):
        '''return the dictionay of context variables for rendering the template.'''
        # call the superclass method 
        context = super().get_context_data()

        # find/add the article to the context
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add the article to the context
        context['article'] = article
        return context


    def form_valid(self, form):
        '''handles the form submission and saves the new comment to the database.'''

        print(form.cleaned_data) #debug
        pk = self.kwargs['pk']  

        # retrieve the article object using the pk
        article = Article.objects.get(pk=pk)

        # attach this article to the comment
        form.instance.article = article  

        # delegate the work to the superclass
        return super().form_valid(form)
    
class UpdateArticleView(UpdateView):
    '''View class to handle update of article'''
    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"

class DeleteCommentView(DeleteView):
    model = Comment
    context_object_name = 'comment'
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
 
 
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.get(pk=pk)
        
        # find the article to which this Comment is related by FK
        article = comment.article
        
        # reverse to show the article page
        return reverse('article', kwargs={'pk':article.pk})
 
 