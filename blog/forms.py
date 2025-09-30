# blog/forms.py

from django import forms
from .models import Article, Comment


class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to the db'''

    class Meta:
        '''associate this form with the Article model'''
        model = Article
        fields = ['author', 'title', 'text', 'image_url']

class CreateCommentForm(forms.ModelForm):
    '''a form to add comments to an article'''

    class Meta:
        '''associate this form with the Comment model'''
        model = Comment
        fields = ['author', 'text']