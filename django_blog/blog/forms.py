# ~/Alx_DjangoLearnLab/django_blog/blog/forms.py

from django import forms
from .models import Post # Import the Post model

class PostForm(forms.ModelForm):
    """
    A ModelForm for the Post model.
    This form will be used for both creating and editing blog posts.
    It automatically generates form fields based on the Post model.
    """
    class Meta:
        model = Post
        # Define the fields that should be included in the form.
        # 'title' and 'content' correspond to your Post model fields.
        # 'author' is typically set automatically in the view for the logged-in user.
        fields = ['title', 'content']
