# ~/Alx_DjangoLearnLab/django_blog/blog/views.py

from django.shortcuts import render, get_object_or_404
from .models import Post # Import your Post model

def post_list(request):
    """
    View to display a list of all published blog posts.
    Posts are ordered by published_date in descending order (newest first).
    """
    posts = Post.objects.all() # Fetch all Post objects
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """
    View to display the details of a single blog post.
    Retrieves a Post object based on its primary key (pk).
    If the post does not exist, it will raise a 404 error.
    """
    post = get_object_or_404(Post, pk=pk) # Fetch a single Post by its primary key
    return render(request, 'blog/post_detail.html', {'post': post})

