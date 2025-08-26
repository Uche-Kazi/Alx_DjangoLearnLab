# ~/Alx_DjangoLearnLab/django_blog/blog/views.py

from django.shortcuts import render, get_object_or_404 # render for templates, get_object_or_404 for fetching objects
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Mixins for access control in class-based views
from django.contrib.auth.models import User # Import Django's built-in User model
from django.views.generic import ( # Import generic class-based views
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment # Import the Post and Comment models from the current app (blog/models.py)
from django.utils import timezone # Import timezone for potential date handling (e.g., setting published_date automatically)
from django.contrib.auth.decorators import login_required

# Class-based view for listing all blog posts
class PostListView(ListView):
    model = Post # Specify the model this view will operate on
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html (e.g., blog/post_list.html is default)
    context_object_name = 'posts' # The variable name used in the template to access the list of posts
    ordering = ['-published_date'] # Order posts by published_date in descending order (most recent first)
    paginate_by = 5 # Display 5 posts per page

# Class-based view for listing posts by a specific user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # Template to render
    context_object_name = 'posts'
    paginate_by = 5

    # Override get_queryset to filter posts by a specific user
    def get_queryset(self):
        # Get the User object based on the username captured in the URL
        # get_object_or_404 raises a 404 error if the user doesn't exist
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # Return posts authored by this user, ordered by most recent first
        # IMPORTANT: Ensure 'published_date' matches the field name in your Post model
        return Post.objects.filter(author=user).order_by('-published_date')

# Class-based view for displaying a single blog post in detail
class PostDetailView(DetailView):
    model = Post # Specify the model this view will operate on
    # Default template name would be blog/post_detail.html

# Class-based view for creating a new blog post
# LoginRequiredMixin ensures that only logged-in users can create posts
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post # Specify the model for which a new instance will be created
    fields = ['title', 'content', 'published_date'] # Fields from the Post model to include in the form
    template_name = 'blog/post_form.html' # Explicitly set template name
    # Default template name would be blog/post_form.html

    # Override form_valid method to assign the current logged-in user as the author
    def form_valid(self, form):
        form.instance.author = self.request.user # Set the author of the post to the current user
        # You could uncomment the line below if you want to automatically set published_date on creation
        # form.instance.published_date = timezone.now()
        return super().form_valid(form) # Call the parent class's form_valid to save the form


# Class-based view for updating an existing blog post
# LoginRequiredMixin ensures only logged-in users can update posts
# UserPassesTestMixin ensures only the author can update their own posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'published_date'] # Include published_date for updating
    template_name = 'blog/post_form.html' # Explicitly set template name
    # Default template name would be blog/post_form.html

    # Override form_valid method (similar to CreateView)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # test_func method for UserPassesTestMixin: checks if the current user is the author of the post
    def test_func(self):
        post = self.get_object() # Get the post object being updated
        if self.request.user == post.author: # Check if the current user is the author
            return True
        return False # If not, deny access

# Class-based view for deleting a blog post
# LoginRequiredMixin ensures only logged-in users can delete posts
# UserPassesTestMixin ensures only the author can delete their own posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # Redirect to the home page after successful deletion
    template_name = 'blog/post_confirm_delete.html' # Default template name (ensure this template exists)

    # test_func method for UserPassesTestMixin: checks if the current user is the author of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Function-based view for the about page
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

