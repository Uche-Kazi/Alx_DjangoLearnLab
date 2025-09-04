from django.shortcuts import render
from .models import Post
from django.db.models import Q # Import Q object for complex lookups

def post_list(request):
    """
    View to display a list of blog posts with optional search functionality.
    """
    # Initialize a queryset of all posts.
    posts = Post.objects.all().order_by('-published_date')
    query = request.GET.get('q')

    if query:
        # If a search query exists, filter the posts.
        # The Q object is used to perform a case-insensitive search across
        # both the 'title' and 'content' fields.
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()

    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/post_list.html', context)
