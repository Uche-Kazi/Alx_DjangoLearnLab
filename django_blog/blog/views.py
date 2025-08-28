# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib import messages # For displaying success/error messages
from django.contrib.auth.models import User # <--- Ensure this import is present
from django.core.mail import send_mail # <--- ADD THIS IMPORT

# Assuming your Post and Comment models are in .models
from .models import Post, Comment
# Assuming your CommentForm is in .forms
from .forms import EmailPostForm, CommentForm

# --- Helper function for comment author check ---
def is_comment_author(user, comment):
    """
    Checks if the given user is the author of the comment.
    """
    return comment.author == user

# --- Existing Post List View ---
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# --- New User-Specific Post List View ---
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html' # Reuse the same list template
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        # Get the username from the URL kwargs
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Post.published.filter(author=user).order_by('-publish')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the user whose posts are being displayed to the context
        context['page_user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context

# --- Modified Post Detail View to include comments ---
def post_detail(request, year, month, day, post):
    """
    Displays a single blog post and handles comment submission.
    """
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    
    new_comment = None # Initialize new_comment to None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            if request.user.is_authenticated:
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, 'Your comment has been posted successfully.')
                return redirect(post.get_absolute_url() + '#comment-' + str(new_comment.pk))
            else:
                messages.error(request, 'You must be logged in to post a comment.')
                return redirect('login')
    else:
        comment_form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'new_comment': new_comment})


# --- View to edit an existing comment ---
@login_required
@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('login'))
def edit_comment(request, comment_id):
    """
    Allows a user to edit their own comment.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if not is_comment_author(request.user, comment):
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect(comment.post.get_absolute_url())

    if request.method == 'POST':
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated successfully.')
            return redirect(comment.post.get_absolute_url() + '#comment-' + str(comment.pk))
        else:
            messages.error(request, 'There was an error updating your comment.')
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/comment/edit.html', {'form': form, 'comment': comment})


# --- View to delete an existing comment ---
@login_required
@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('login'))
def delete_comment(request, comment_id):
    """
    Allows a user to delete their own comment.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if not is_comment_author(request.user, comment):
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect(comment.post.get_absolute_url())

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Your comment has been deleted successfully.')
        return redirect(comment.post.get_absolute_url())
    
    return render(request, 'blog/comment/delete_confirm.html', {'comment': comment})


# --- Post Share View ---
def post_share(request, post_id):
    """
    Allows users to share a blog post via email.
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']]) # Change 'your_account@gmail.com' to your email
            sent = True
        else:
            messages.error(request, 'There was an error sending the email. Please check the form.')
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
