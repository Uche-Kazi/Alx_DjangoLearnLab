from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    """
    A view to display a list of published blog posts.
    """
    # Use Post.objects.filter() to get a queryset of all published posts.
    # The 'status' field is assumed to exist on the Post model.
    posts = Post.objects.filter(status='published').order_by('-publish')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    """
    A view to display a single blog post.
    """
    post = get_object_or_404(Post,
                             status='published',
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post_detail.html', {'post': post})
