# blog/forms.py

from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    """
    A form for sharing a post via email.
    It includes fields for the sender's name and email,
    the recipient's email, and optional comments.
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    """
    A ModelForm for creating new comments.
    It automatically saves the data to the Comment model.
    """
    class Meta:
        model = Comment
        # The 'content' field is the only one users will directly input.
        # 'post' and 'author' will be set in the view.
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }

