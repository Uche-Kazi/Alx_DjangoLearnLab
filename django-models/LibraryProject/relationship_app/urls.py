from django.urls import path
from . import views # Import views from the current app

# Import the class-based view directly
from .views import LibraryDetailView

app_name = 'relationship_app' # Namespace for this app's URLs

urlpatterns = [
    # URL for the function-based view (list all books)
    # Example URL: /books/
    path('books/', views.book_list, name='book_list'),

    # URL for the class-based view (library details)
    # Example URL: /libraries/1/ (where 1 is the library's primary key/ID)
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
