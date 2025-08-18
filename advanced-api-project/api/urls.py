# ~/Alx_DjangoLearnLab/advanced-api-project/api/urls.py

from django.urls import path
from .views import BookListCreateView, BookDetailView # Import your views

urlpatterns = [
    # URL for listing all books and creating a new book.
    # Maps to BookListCreateView.
    path('books/', BookListCreateView.as_view(), name='book-list-create'),

    # URL for retrieving, updating, or deleting a single book by its primary key (ID).
    # Maps to BookDetailView.
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]
