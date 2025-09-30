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
    def get_all_posts(self):
        '''Return a QuerySet of posts made by this profile.'''
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
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
    
class Photo(models.Model):
    '''Model representing a photo in a post.'''

    # define data fields of the Photo model
    post = models.ForeignKey(Post, on_delete=models.CASCADE) #foreign key to Post model
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True) #set the published date automatically  
    
    def __str__(self):
        '''String for representing the Model object.'''
        return f'Photo uploaded with {self.post} at {self.image_url} posted {self.timestamp}'