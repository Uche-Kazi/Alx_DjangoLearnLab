# my_library_project/bookshelf/forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    A ModelForm for the Book model.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'isbn']
