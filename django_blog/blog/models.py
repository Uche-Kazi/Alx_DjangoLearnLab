# ~/Alx_DjangoLearnLab/django_blog/blog/models.py

from django.db import models
from django.contrib.auth import get_user_model # Import get_user_model to reference the User model
from django.utils import timezone # Add this import for timezone.now()

# Get the currently active user model. This is the recommended way to
# reference the User model, especially if you plan to use a custom user model later.
User = get_user_model()

class Post(models.Model):
    """
    Model representing a blog post.
    Each post has a title, content, a publication date, and an author.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Make published_date nullable for draft functionality.
    # It will be set explicitly when a post is published.
    published_date = models.DateTimeField(null=True, blank=True)
    # ForeignKey to Django's User model.
    # on_delete=models.CASCADE means that if a User is deleted, all their posts will also be deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        # Order posts by published_date in descending order by default.
        # This means newer posts will appear first.
        # For drafts (where published_date is null), they might appear differently,
        # which is handled by the view separating drafts.
        ordering = ['-published_date']

    def __str__(self):
        """
        String representation of the Post model.
        """
        return self.title

