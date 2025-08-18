# ~/Alx_DjangoLearnLab/api/admin.py

from django.contrib import admin
from .models import Author, Book

# Register the Author model so it's accessible in the Django admin.
# This allows you to create and manage authors.
admin.site.register(Author)

# Register the Book model so it's accessible in the Django admin.
# This allows you to create and manage books, linking them to authors.
admin.site.register(Book)
