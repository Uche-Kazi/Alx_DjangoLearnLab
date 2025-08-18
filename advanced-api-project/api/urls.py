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
    # List all books (GET)
    path('books/', BookListView.as_view(), name='book-list'),
    # Create a new book (POST) - separate endpoint as per individual view requirements
    path('books/create/', BookCreateView.as_view(), name='book-create'),

    # Retrieve, Update, Delete a single book by ID
    path('books/<int:pk>/', BookRetrieveView.as_view(), name='book-retrieve'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDestroyView.as_view(), name='book-delete'),
]
