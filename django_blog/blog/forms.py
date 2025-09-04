from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """
    A form for users to submit comments on blog posts.
    It uses the Comment model and only includes the 'name', 'email', and 'body' fields.
    """
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class PostSearchForm(forms.Form):
    """
    A simple form for searching blog posts by keywords.
    """
    query = forms.CharField()
