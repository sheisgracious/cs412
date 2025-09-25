from django.contrib import admin

# Register your models here.
from .models import Article
admin.site.register(Article)

from mini_insta.models import Profile
admin.site.register(Profile)