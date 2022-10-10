from django.contrib import admin

from blog_app.models import Post
from .models import Like, Post, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)