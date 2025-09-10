from django.db import models
<<<<<<< HEAD
from django.conf import settings

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
=======
from django.contrib.auth import get_user_model

# Get the custom user model defined in settings
User = get_user_model()

class Post(models.Model):
    """
    Represents a user's post on the platform.
    """
    # A foreign key to the User model, linking the post to its creator.
    # The 'on_delete=models.CASCADE' ensures that if a user is deleted, their posts are also deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    # The main content of the post.
    content = models.TextField()

    # An optional image field for the post. 'upload_to' specifies the directory
    # where uploaded images will be stored.
    image = models.ImageField(upload_to='posts/', null=True, blank=True)

    # Automatically sets the timestamp when the post is created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Post model."""
        return f'Post by {self.user.username} on {self.created_at.strftime("%Y-%m-%d")}'

class Comment(models.Model):
    """
    Represents a comment on a post.
    """
    # Foreign key to the User model, linking the comment to its author.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    # Foreign key to the Post model, linking the comment to a specific post.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    # The content of the comment.
    content = models.TextField()

    # Automatically sets the timestamp when the comment is created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Comment model."""
        return f'Comment by {self.user.username} on {self.post.id}'

class Like(models.Model):
    """
    Represents a 'like' on a post.
    """
    # Foreign key to the User model, linking the like to a user.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    # Foreign key to the Post model, linking the like to a specific post.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    
    # Ensures that a user can only 'like' a specific post once.
    class Meta:
        unique_together = ('user', 'post',)

    def __str__(self):
        """String representation of the Like model."""
        return f'{self.user.username} liked Post {self.post.id}'
>>>>>>> 1bbf6deb52f8e292397419e3b8a1dc2c44b8c68e
