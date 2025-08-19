# ~/Alx_DjangoLearnLab/advanced-api-project/api/urls.py

from django.urls import path
from .views import (
    BookListView,
    BookCreateView,
    BookRetrieveView,
    BookUpdateView,
    BookDestroyView
)

urlpatterns = [
    # List all books (GET) - unauthenticated allowed
    path('books/', BookListView.as_view(), name='book-list'),

    # Create a new book (POST) - authenticated only
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # Retrieve a single book (GET) - unauthenticated allowed
    path('books/<int:pk>/', BookRetrieveView.as_view(), name='book-retrieve'),

    # Update an existing book (PUT/PATCH) - authenticated only, expects 'id' in request body
    # This URL does NOT have a PK in the path, as per our custom view's get_object.
    path('books/update/', BookUpdateView.as_view(), name='book-update'),

    # Delete a book (DELETE) - authenticated only, expects 'id' in query params or request body
    # This URL does NOT have a PK in the path, as per our custom view's get_object.
    path('books/delete/', BookDestroyView.as_view(), name='book-delete'),
]

