# mini_insta/views.py 
# Gracious Ogyiri Asare- gpoa@bu.edu

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.urls import reverse
from .forms import CreatePostForm, UpdateProfileForm

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
        
        # image_url = self.request.POST.get('image_url', '').strip()
        # if image_url:
        #     Photo.objects.create(post=self.object, image_url=image_url)

        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return superclass

class UpdateProfileView(UpdateView):
    '''View class to handle update of profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    '''Delete a post'''
    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    
    def get_context_data(self, **kwargs):
        '''add post and profile to context.'''
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        '''redireect to the profile page'''
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)

        # call reverse to get the URL for the progile 
        return reverse('show_profile', kwargs={'pk': post.profile.pk})

class UpdatePostView(UpdateView):
    '''Update a post'''
    model = Post
    template_name = 'mini_insta/update_post_form.html'
    fields = ['caption']
    
    def get_success_url(self):
        '''redireect to the profile page'''
        return reverse('show_post', kwargs={'pk': self.object.pk})
    
class ShowFollowersDetailView(DetailView):
    '''Show followers'''
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'  

class ShowFollowingDetailView(DetailView):
    '''show following'''
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'  

class PostFeedListView(ListView):
    """show post feed for a profile"""
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

class SearchView(ListView):
    '''display search results'''
    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request and dispatch to appropriate template'''
        self.query = request.GET.get('query', '').strip()
        
        if not self.query:
            context = {
                'profile': Profile.objects.get(pk=kwargs['pk'])
            }
            return render(request, 'mini_insta/search.html', context)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''get posts that match the search'''
        posts = Post.objects.filter(caption__icontains=self.query)
        return posts

    def get_context_data(self, **kwargs):
        '''add profiles and query to context'''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        context['query'] = self.query
        
        profiles = Profile.objects.filter(
            models.Q(username__icontains=self.query) |
            models.Q(display_name__icontains=self.query) |
            models.Q(bio_text__icontains=self.query)
        )
        context['profiles'] = profiles
        
        return context