# ~/Alx_DjangoLearnLab/advanced-api-project/api/views.py

from rest_framework import generics # Import DRF's generic views
from rest_framework import permissions # Import DRF's permission classes
from .models import Book # Import the Book model
from .serializers import BookSerializer # Import the BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    API view for listing all books and creating a new book.

    - GET /books/: Retrieves a list of all books.
    - POST /books/: Creates a new book.
        - Requires authentication.
        - Unauthenticated users have read-only access (can view list, but not create).
    """
    queryset = Book.objects.all() # Define the queryset for retrieving Book objects
    serializer_class = BookSerializer # Specify the serializer to use for Book objects
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Allow read for all, write for authenticated

    # Customization Instruction (from Step 3):
    # The generic views automatically handle validation defined in BookSerializer.
    # For POST and PUT, the serializer's validate_publication_year will be called.
    # No explicit custom methods needed here for validation handling beyond serializer.

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a single book.

    - GET /books/<int:pk>/: Retrieves a single book by its primary key (ID).
    - PUT /books/<int:pk>/: Updates an existing book.
        - Requires authentication.
    - PATCH /books/<int:pk>/: Partially updates an existing book.
        - Requires authentication.
    - DELETE /books/<int:pk>/: Deletes a book.
        - Requires authentication.
        - Unauthenticated users have read-only access (can view detail, but not update/delete).
    """
    queryset = Book.objects.all() # Define the queryset to find the specific Book object
    serializer_class = BookSerializer # Specify the serializer to use
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Allow read for all, write/delete for authenticated

    # Customization Instruction (from Step 3):
    # Similar to ListCreateView, validation is handled by the serializer.
    # Permissions are handled by permission_classes.
    # No additional custom methods for form submission/validation are typically needed for these generic views.
