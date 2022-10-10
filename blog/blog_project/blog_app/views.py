from http.client import HTTPResponse
import imp
from multiprocessing import context
from unicodedata import name
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Like
from .forms import CommentForm

# Create your fxn views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog_app/home.html', context)

#likes comment not working
def like_post(request, post_id):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
            
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
            
        like, created = Like.objects.get_or_created(user=user, post_id=post_id)
            
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'like'
        like.save()
    return redirect(reverse(request, 'post-detail'))

#class based views for the fuction view of home
class PostListView(ListView):
    model = Post
    template_name = 'blog_app/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] #display the lastest post at the top
    paginate_by = 3 #to paginate the pages to contain 2 post per page

#filter all the post by a certain user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog_app/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3 #to paginate the pages to contain 2 post per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
#class based view for the individual post object
class PostDetailView(DetailView):
    model = Post
    
    form = CommentForm    
      
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={'pk': post.pk}))
        
    def get_context_data(self, **kwargs):
        post_comments_count = Comment.objects.all().filter(post=self.object.id).count()
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'post_comments_count': post_comments_count,
        })
        return context    
 

#class based view to create new posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    #assign the author of the new post to the logged in user using the form valid method
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#Class based view to update post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
    #setting the current logged in user to be the author of the post to be updated
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    #this ensures that a logged in user cannot edit a post he/she did not create
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

#a view to delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home/' #redirect to the home page when the post is deleted 
    
    #this ensures that a logged in user cannot edit a post he/she did not create
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog_app/about.html', {'title': 'About'})