# ~/Alx_DjangoLearnLab/django_blog/blog/forms.py
from django import forms
from .models import Post, Comment # Import the Comment model as well

class PostForm(forms.ModelForm):
    """
    A Django ModelForm for the Post model.
    This form will be used for creating and updating blog posts.
    """
    class Meta:
        """
        Meta options for the PostForm.
        Defines the model the form is associated with and the fields to include.
        """
        model = Post
        # Specify the fields from the Post model that should be included in the form.
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post content here...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title...'}),
        }
        help_texts = {
            'title': 'Keep your title concise and engaging.',
            'content': 'Write the full content of your blog post here. Markdown is supported!',
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
        }

class CommentForm(forms.ModelForm):
    """
    A Django ModelForm for the Comment model.
    This form will be used for adding comments to blog posts.
    """
    class Meta:
        """
        Meta options for the CommentForm.
        Defines the model the form is associated with and the fields to include.
        """
        model = Comment
        # Only allow the user to input the text content of the comment.
        # The 'post' and 'author' will be set automatically in the view.
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Join the discussion...'}),
        }
        labels = {
            'text': 'Your Comment',
        }
