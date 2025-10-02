# mini_insta/views.py 
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from django.urls import reverse
from .forms import CreatePostForm

# Create your views here.
class ProfileListView(ListView):
    '''Display all profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles' 
    ordering = ['-join_date']  

class ProfileDetailView(DetailView):
    '''Display single profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'  

class PostDetailView(DetailView):
    '''Display single post.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    def get_success_url(self):
        '''provide a URL to redirect to after the form is successfully processed.'''
        pk = self.kwargs['pk']  
        return reverse('show_profile', kwargs={'pk': pk})   
    
    def get_context_data(self):
        '''return the dictionary of context variables for rendering the template.'''
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile
        superclass = super().form_valid(form)
        
        image_url = self.request.POST.get('image_url', '').strip()
        if image_url:
            Photo.objects.create(post=self.object, image_url=image_url)

        return superclass
