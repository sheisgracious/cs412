from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
import random

# Create your views here.



class ShowAllView(ListView):
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' #plural name similar to model name- contains many instances of the model
    ordering = ['-published']  # Order by published date descending

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
 
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
 
 
        return super().dispatch(request, *args, **kwargs)

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
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''Create a new article.
    1. Display a HTML form to the user (GET)
    2. Process the form submission and store the new Article object (POST)
    '''
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def form_valid(self, form):
        '''handles the form submission and saves the new article to the database.'''

        print(f'CreateArtleView.form_valid(): {form.cleaned_data}') #debug
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
        form.instance.user = user
 
        return super().form_valid(form)
        
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

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
 
class RegistrationView(CreateView):
    '''View class to handle user registration'''
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
 
class UserRegistrationView(CreateView):
    '''show registration form to create a new User.'''
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')