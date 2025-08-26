# ~/Alx_DjangoLearnLab/django_blog/blog/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse # Import reverse to get URL by name

User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    # Add this method to define the canonical URL for a Post object
    def get_absolute_url(self):
        # This will return the URL to the detail page of the specific post
        # The 'pk' (primary key) of the post is used to construct the URL
        return reverse('blog:post-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'
