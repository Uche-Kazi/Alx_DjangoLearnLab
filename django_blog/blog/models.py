# blog/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    """
    A custom manager to retrieve all published posts.
    It filters the queryset to only include posts with status='published'.
    """
    def get_queryset(self):
        # We define Post later, so reference it as a string
        return super().get_queryset().filter(status='PB') # Use 'PB' as the literal value for PUBLISHED

class Post(models.Model):
    """
    The main Post model for the blog application.
    It contains fields for the post's title, body, publication details, and more.
    """
    # A class to define choices for the post status
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    objects = models.Manager()  # The default Django manager
    published = PublishedManager()  # Our custom manager
    tags = TaggableManager() # The tag manager for the 'taggit' library

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

class Comment(models.Model):
    """
    Model representing a comment on a blog post, linked to a User.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The blog post this comment belongs to."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1,                   # Default user ID (e.g., your superuser's ID)
        related_name='comments',
        help_text="The user who wrote this comment."
    )
    content = models.TextField(
        default="Default comment content", # Default string content
        help_text="The main text content of the comment."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        # default=timezone.now,       # <--- REMOVED THIS CONFLICTING LINE
        help_text="The date and time when the comment was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        # default=timezone.now,       # <--- REMOVED THIS CONFLICTING LINE
        help_text="The date and time when the comment was last updated."
    )
    active = models.BooleanField(
        default=True,
        help_text="Indicates if the comment is approved and visible."
    )

    class Meta:
        ordering = ['created_at'] # Order comments by creation date, oldest first
        indexes = [
            models.Index(fields=['created_at']),
        ]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        """
        String representation of the Comment object.
        """
        # Truncate content for a cleaner string representation
        return f'Comment by {self.author.username} on "{self.post.title}"' \
               f': {self.content[:50]}{"..." if len(self.content) > 50 else ""}'

    def get_absolute_url(self):
        """
        Returns the URL to access a particular comment instance.
        """
        # This will likely redirect to the post detail page where the comment is displayed
        return reverse('blog:post_detail', args=[
            self.post.publish.year,
            self.post.publish.month,
            self.post.publish.day,
            self.post.slug
        ])

