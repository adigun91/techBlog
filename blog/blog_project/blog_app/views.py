import imp
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import CommentForm

# Create your fxn views here.
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog_app/home.html', context)

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
class PostDetailView(DetailView, LoginRequiredMixin):
    model = Post
    
    form = CommentForm    
      
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
             
            return redirect(reverse("post", kwargs={
                'content': post.content
            }))
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
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