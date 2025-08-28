# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Import Mixins

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

# --- Helper function for comment author check (Still useful for function-based views if any remain) ---
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

# --- User-Specific Post List View ---
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Post.published.filter(author=user).order_by('-publish')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context

# --- Post Detail View (Modified to handle comments indirectly) ---
def post_detail(request, year, month, day, post_slug): # Renamed 'post' to 'post_slug' for clarity
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=post_slug)

    comments = post.comments.filter(active=True)
    # The comment form will now be handled by CommentCreateView.
    # We still need to pass a blank form for display if the user is authenticated.
    comment_form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form, # Pass the blank form for display
                   })


# --- NEW: Class-Based View for Creating Comments ---
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' # A generic template for the form

    def form_valid(self, form):
        # Set the author and post before saving
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        form.instance.author = self.request.user
        form.instance.post = post
        messages.success(self.request, 'Your comment has been posted successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the post detail page
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.get_absolute_url() + '#comments-section' # Redirect to comments section


# --- NEW: Class-Based View for Updating Comments ---
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' # Reuse the generic form template

    def test_func(self):
        # Ensure only the author can update their comment
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        # Redirect back to the post detail page
        comment = self.get_object()
        messages.success(self.request, 'Your comment has been updated successfully.')
        return comment.post.get_absolute_url() + '#comment-' + str(comment.pk)


# --- NEW: Class-Based View for Deleting Comments ---
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html' # A generic confirmation template

    def test_func(self):
        # Ensure only the author can delete their comment
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        # Redirect back to the post detail page after deletion
        comment = self.get_object()
        messages.success(self.request, 'Your comment has been deleted successfully.')
        return comment.post.get_absolute_url() + '#comments-section' # Redirect to comments section

# --- Post Share View (remains the same) ---
def post_share(request, post_id):
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
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True
        else:
            messages.error(request, 'There was an error sending the email. Please check the form.')
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

