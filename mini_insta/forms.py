# mini_insta/forms.py
from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the db'''

    class Meta:
        '''associate this form with the Post model'''
        model = Post
        fields = ['caption']

    