# mini_insta/models.py
# Gracious Ogyiri Asare- gpoa@bu.edu

# define data models for the mini_insta app
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''Model representing a user profile.'''

    # define data fields of the Profile model
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True) #set the joined date automatically
    user = models.ForeignKey(User, on_delete=models.CASCADE) #foreign key to User model

    
    def __str__(self):
        '''String for representing the Model object.'''
        return f'{self.username} is displayed as {self.display_name} and has bio: {self.bio_text}'
    def get_all_posts(self):
        '''Return a QuerySet of posts made by this profile.'''
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts
    def get_absolute_url(self):
        '''return url to access the profile'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        '''return a list of profiles who are following this profile'''
        followers = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in followers]
    def get_num_followers(self):
        '''return the count of followers'''
        followers = Follow.objects.filter(profile=self)
        return followers.count()
    def get_following(self):
        '''return the profiles following'''
        following = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in following]
    def get_num_following(self):
        '''return the count of following'''
        following = Follow.objects.filter(follower_profile=self)
        return following.count()
    def get_post_feed(self):
        """return posts from profiles this profile is following"""
        following_profiles = [f.profile for f in Follow.objects.filter(follower_profile=self)]
        posts = Post.objects.filter(profile__in=following_profiles)
        return posts


class Post(models.Model):
    '''Model representing a post.'''

    # define data fields of the Post model
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) #foreign key to Profile model
    timestamp = models.DateTimeField(auto_now=True) #set the published date automatically  
    caption = models.TextField(blank=True)
    
    def __str__(self):
        '''String for representing the Model object.'''
        return f'{self.caption} made by {(self.profile).display_name} at {self.timestamp}' #for easier read
    
    def get_all_photos(self):
        '''Return a QuerySet of photos in this post.'''
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_absolute_url(self):
        '''return the url to access this post.'''
        return reverse('show_post', kwargs={'pk': self.pk})
    
    def get_likes(self):
        """return a list profiles who liked this post"""
        likes = Like.objects.filter(post=self)
        return [l.profile for l in likes]
    

class Photo(models.Model):
    '''Model representing a photo in a post.'''

    # define data fields of the Photo model
    post = models.ForeignKey(Post, on_delete=models.CASCADE) #foreign key to Post model
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True) #set the published date automatically  
    
    def __str__(self):
        '''String for representing the Model object.'''
        image_url = self.get_image_url()
        if image_url:
            return f'Photo uploaded with {self.post} at {image_url} posted at {self.timestamp}'
        else:
            return f'Photo uploaded with {self.post} posted {self.timestamp}'
    
    def get_image_url(self):
        '''Return the URL to image'''
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        return None
    
class Follow(models.Model):
    '''Model representing followers of a profile'''
    # define data fields of the Follow model
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile") #foreign key to Profile model
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile") #foreign key to Profile model
    timestamp = models.DateTimeField(auto_now_add=True) #set the published date automatically  

    def __str__(self):
        '''String for representing the Model object.'''
        return f"{self.follower_profile.username} follows {self.profile.username} since {self.timestamp}"
        
class Comment(models.Model):
    '''Model represent comments for a post'''
    # define data fields of the Comment model
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True) #temporary
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True) #temp
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.profile.username} for {self.post} on {self.timestamp} saying {self.text}'


class Like(models.Model):
    '''Model representing likes for a post'''

    # define data fields of the Like model
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True) #temporary
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True) #temp
    timestamp = models.DateTimeField(auto_now=True)  

    def __str__(self):
        '''string representation'''
        return f'{self.profile.username} liked post {self.post.id} at {self.timestamp}'
    