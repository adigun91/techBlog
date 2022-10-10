import imp
from pickle import NONE
from time import timezone
from tkinter import CASCADE
from django.db import models
from django.utils import timezone #imported because of the timezone function we used for the date posted
from django.contrib.auth.models import User #imported becuase we want to associated the post to the User who created the post from the User model
from django.urls import reverse

# Create your models here.
    
#Add the Post model below
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name="liked")
    
    def __str__(self):
        return self.title

    @property
    def num_likes(self):
        return self.liked.all().count()

    #get the absolute url of the post and redirect the newly created post to the post detail
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})    
    
    
#Add the comment model below
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    comment = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    
#Add the likes button
LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)
   
   def __str__(self):
       return str(self.post)
    
  