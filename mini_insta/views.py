# mini_insta/views.py 
# Gracious Ogyiri Asare- gpoa@bu.edu

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from django.urls import reverse
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class MethodLoginRequiredMixin(LoginRequiredMixin):
    '''Method to require login '''
    
    def get_login_url(self):
        '''return login url'''
        return reverse('login')
    
    def get_profile(self):
        '''get profile of user logged in'''
        return Profile.objects.get(user=self.request.user)
    
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

class CreatePostView(MethodLoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    def get_success_url(self):
        '''provide a URL to redirect to after the form is successfully processed.'''
        profile = self.get_profile()
        return reverse('show_profile', kwargs={'pk': profile.pk})   
    
    def get_context_data(self, **kwargs):
        '''return the dictionary of context variables for rendering the template.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

    def form_valid(self, form):
        pk = self.kwargs['pk']

        profile = self.get_profile()
        form.instance.profile = profile
        superclass = super().form_valid(form)
        
        # image_url = self.request.POST.get('image_url', '').strip()
        # if image_url:
        #     Photo.objects.create(post=self.object, image_url=image_url)

        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return superclass

class UpdateProfileView(MethodLoginRequiredMixin, UpdateView):
    '''View class to handle update of profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        '''get profile of user logged in'''
        return self.get_profile()

class DeletePostView(MethodLoginRequiredMixin, DeleteView):
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

class UpdatePostView(MethodLoginRequiredMixin, UpdateView):
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

class PostFeedListView(MethodLoginRequiredMixin, ListView):
    """show post feed for a profile"""
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        profile = self.get_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

class SearchView(MethodLoginRequiredMixin, ListView):
    '''display search results'''
    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request and dispatch to appropriate template'''
        self.query = request.GET.get('query', '').strip()
        
        if not self.query:
            context = {
                'profile': self.get_profile()
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
        context['profile'] = self.get_profile()
        context['query'] = self.query
        
        profiles = Profile.objects.filter(
            models.Q(username__icontains=self.query) |
            models.Q(display_name__icontains=self.query) |
            models.Q(bio_text__icontains=self.query)
        )
        context['profiles'] = profiles
        
        return context
    

class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if not user_form.is_valid(form):
            return self.form_invalid(form)
        user = user_form.save(form)
        form.instance.user = user
        return super().form_valid(form)







class CreateProfileView(CreateView):
    '''create a new profile with user registration'''
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'
    
    def get_context_data(self, **kwargs):
        '''override context'''
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''process the user and profile creation'''
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class FollowView(MethodLoginRequiredMixin, TemplateView):
    '''folow a profile'''
    def dispatch(self, request, *args, **kwargs):
        following = Profile.objects.get(pk=kwargs['pk'])
        user_profile = self.get_profile()
        
        if following != user_profile: #users cant follow themselves
            if not Follow.objects.filter(
                follower_profile=user_profile,
                profile=following
            ).exists():
                Follow.objects.create(
                    follower_profile=user_profile,
                    profile=following
                )
        return redirect('show_profile', pk=following.pk)
    
class UnfollowView(MethodLoginRequiredMixin, TemplateView):
    '''Unfollow profile'''
    def dispatch(self, request, *args, **kwargs):
        '''Delete follow relationship'''
        unfollow = Profile.objects.get(pk=kwargs['pk'])
        user_profile = self.get_profile()
        
        Follow.objects.filter(
            follower_profile=user_profile,
            profile=unfollow
        ).delete()
        return redirect('show_profile', pk=unfollow.pk)

class LikeView(MethodLoginRequiredMixin, TemplateView):
    '''Like a post'''
    def dispatch(self, request, *args, **kwargs):
        '''Create like for a post'''
        post = Post.objects.get(pk=kwargs['pk'])
        user_profile = self.get_profile()
        
        if post.profile != user_profile: #users can't like their posts
            if not Like.objects.filter(
                profile=user_profile,
                post=post
            ).exists():
                Like.objects.create(
                    profile=user_profile,
                    post=post
                )
        
        return redirect('show_post', pk=post.pk)

class UnlikeView(MethodLoginRequiredMixin, TemplateView):
    '''Unlike a post'''
    def dispatch(self, request, *args, **kwargs):
        '''Delete like for a post'''
        post = Post.objects.get(pk=kwargs['pk'])
        user_profile = self.get_profile()
        
        Like.objects.filter(
            profile=user_profile,
            post=post
        ).delete()
        
        return redirect('show_post', pk=post.pk)