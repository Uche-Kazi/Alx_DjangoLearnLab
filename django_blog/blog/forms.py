from django import forms

# Import the new widget for handling tags
from tag_manager.widgets import TagWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    """
    class Meta:
        model = Post
        fields = ('title', 'slug', 'author', 'content', 'status', 'tags')
        
        # Configure the widgets to use the custom TagWidget for the 'tags' field.
        # This tells the form to render the tags using our custom-built widget.
        widgets = {
            'tags': TagWidget(),
        }

class CommentForm(forms.ModelForm):
    """
    Form for creating comments on blog posts.
    """
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
