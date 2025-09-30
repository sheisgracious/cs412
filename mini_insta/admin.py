from django.contrib import admin

# Register your models here.
from mini_insta.models import Profile, Post, Photo
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
