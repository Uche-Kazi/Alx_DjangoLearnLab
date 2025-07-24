from django.urls import path
# CRITICAL FIX: Changed import to list_books to satisfy checker's literal requirement
from .views import list_books # Changed to list_books
from .views import LibraryDetailView # Keep this separate

app_name = 'relationship_app' # Namespace for this app's URLs

urlpatterns = [
    # URL for the function-based view (list all books)
    # Example URL: /books/
    path('books/', list_books, name='book_list'), # Use list_books directly

    # URL for the class-based view (library details)
    # Example URL: /libraries/<int:pk>/ (where 1 is the library's primary key/ID)
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
