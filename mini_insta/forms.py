# mini_insta/forms.py
# Gracious Ogyiri Asare- gpoa@bu.edu
from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the db'''

    class Meta:
        '''associate this form with the Post model'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to handle an update to a profile'''
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
