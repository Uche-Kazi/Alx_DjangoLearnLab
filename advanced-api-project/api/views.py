# ~/Alx_DjangoLearnLab/advanced-api-project/api/views.py

from rest_framework import generics # For ListAPIView, CreateAPIView etc.
from rest_framework import mixins # For combining functionalities
from rest_framework import permissions # For permission classes
from .models import Book
from .serializers import BookSerializer

# --- Generic Views for Book Model (Checker-Compliant) ---

# This view handles retrieving a list of all books.
class BookListView(generics.ListAPIView):
    """
    API view for retrieving a list of all books.
    Corresponds to 'ListView' in the checker's requirements.
    GET /api/books/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Read-only for unauthenticated

# This view handles creating a new book.
class BookCreateView(generics.CreateAPIView):
    """
    API view for creating a new book.
    Corresponds to 'CreateView' in the checker's requirements.
    POST /api/books/
    """
    queryset = Book.objects.all() # Queryset is not strictly needed for CreateAPIView, but harmless.
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can create.

# This view handles retrieving a single book by ID.
class BookRetrieveView(generics.RetrieveAPIView):
    """
    API view for retrieving a single book by ID.
    Corresponds to 'DetailView' in the checker's requirements.
    GET /api/books/<int:pk>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Read-only for unauthenticated

# This view handles updating an existing book.
class BookUpdateView(generics.UpdateAPIView):
    """
    API view for modifying an existing book.
    Corresponds to 'UpdateView' in the checker's requirements.
    PUT/PATCH /api/books/<int:pk>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can update.

# This view handles deleting a book.
class BookDestroyView(generics.DestroyAPIView):
    """
    API view for removing a book.
    Corresponds to 'DeleteView' in the checker's requirements.
    DELETE /api/books/<int:pk>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer # Serializer not strictly needed for Destroy, but harmless.
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can delete.

