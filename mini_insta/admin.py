from django.contrib import admin

# Register your models here.
from mini_insta.models import *
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)

