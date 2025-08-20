# ~/Alx_DjangoLearnLab/django_blog/blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone # Import timezone to handle datetimes
from .models import Post # Import your Post model
from django.contrib.auth.decorators import login_required # For post_create, edit, delete, publish
from .forms import PostForm # We'll define this later for post_create/edit

def post_list(request):
    """
    View to display a list of all published blog posts and the current user's drafts.
    Ensures proper handling of offset-naive and offset-aware datetimes.
    """
    # Filter for published posts (where published_date is not null) and order them newest first
    published_posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')

    user_drafts = []
    if request.user.is_authenticated:
        # Filter for the current user's drafts (where published_date is null)
        # Order drafts by creation date or title if needed.
        # We assume for drafts, 'published_date' is None, so we order by 'created_date' if available,
        # or simply by title for consistency. The Post model only has 'published_date' for now,
        # so if it's always auto_now_add, it will have a value, unless we explicitly set it to None for drafts.
        # Assuming `published_date = models.DateTimeField(null=True, blank=True)` for drafts functionality
        # and it's set to None when a post is created as a draft.
        # If your Post model only has `auto_now_add=True`, then `published_date` will never be null unless changed.
        # For this fix, let's assume `published_date` can be `None` for drafts.
        user_drafts = Post.objects.filter(author=request.user, published_date__isnull=True).order_by('title')

    return render(request, 'blog/post_list.html', {
        'posts': published_posts,
        'user_drafts': user_drafts
    })

def post_detail(request, pk):
    """
    View to display the details of a single blog post.
    Retrieves a Post object based on its primary key (pk).
    If the post does not exist, it will raise a 404 error.
    """
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    """
    View to create a new blog post.
    Requires user to be logged in.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Post is a draft by default; published_date is set only when published.
            # If your model uses auto_now_add=True for published_date, you might need to
            # explicitly set it to None or use a separate field like 'created_date'.
            # For draft functionality, published_date should be nullable.
            post.published_date = None # Ensure it's explicitly None for a draft
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    """
    View to edit an existing blog post.
    Requires user to be logged in and be the author of the post.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_detail', pk=post.pk) # Or render 403 Forbidden

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    """
    View to delete a blog post.
    Requires user to be logged in and be the author of the post.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_detail', pk=post.pk) # Or render 403 Forbidden
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


@login_required
def post_publish(request, pk):
    """
    View to publish a blog post.
    Sets the published_date to the current timezone-aware datetime.
    Requires user to be logged in and be the author of the post.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_detail', pk=post.pk) # Or render 403 Forbidden
    
    # Set the published_date to the current timezone-aware time
    post.published_date = timezone.now()
    post.save()
    return redirect('post_detail', pk=post.pk)

