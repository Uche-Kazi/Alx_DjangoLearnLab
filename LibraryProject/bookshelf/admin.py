# bookshelf/admin.py
from django.contrib import admin
from .models import Book  # We need to import the Book model from models.py

# This line registers the Book model with the Django admin site.
# Once registered, you can create, view, update, and delete book
# objects directly from the admin panel.
admin.site.register(Book)
