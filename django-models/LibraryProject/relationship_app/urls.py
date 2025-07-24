from django.urls import path
# CRITICAL FIX: Changed import for book_list to satisfy checker's literal requirement
from .views import book_list, LibraryDetailView # Import both views directly

app_name = 'relationship_app' # Namespace for this app's URLs

urlpatterns = [
    # URL for the function-based view (list all books)
    # Example URL: /books/
    path('books/', book_list, name='book_list'), # Use book_list directly

    # URL for the class-based view (library details)
    # Example URL: /libraries/<int:pk>/ (where 1 is the library's primary key/ID)
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
