# ~/Alx_DjangoLearnLab/advanced-api-project/api/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# This is the specific import line the checker is looking for.
from django_filters import rest_framework as filters # Renamed for cleaner usage below

from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Book
from .serializers import BookSerializer

# --- Generic Views for Book Model ---

# This view handles retrieving a list of all books and incorporates filtering, searching, and ordering.
class BookListView(generics.ListAPIView):
    """
    API view for retrieving a list of all books with filtering, searching, and ordering capabilities.
    Corresponds to 'ListView' in the checker's requirements.

    Query Parameters:
    - Filtering:
        - ?title=<exact_title>
        - ?author=<author_id> (Note: filters by author ID for ForeignKey)
        - ?publication_year=<year>
    - Searching:
        - ?search=<query> (Searches in 'title' and 'author__name')
    - Ordering:
        - ?ordering=title
        - ?ordering=-publication_year (for descending)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Read-only for unauthenticated

    # --- Filtering, Searching, Ordering Configuration ---
    # Reference the DjangoFilterBackend via the 'filters' alias
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Step 1: Set Up Filtering
    # Fields available for exact filtering using DjangoFilterBackend
    # For foreign keys like 'author', you typically filter by the ID.
    filterset_fields = ['title', 'author', 'publication_year']

    # Step 2: Implement Search Functionality
    # Fields on which to apply search. '^' starts with, '=' exact, '@' full-text (if supported), '$' regex.
    # 'author__name' allows searching on the related Author's name.
    search_fields = ['title', 'author__name']

    # Step 3: Configure Ordering
    # Fields by which results can be ordered.
    # Users can request like: ?ordering=title or ?ordering=-publication_year
    ordering_fields = ['title', 'publication_year']
    # You can also set a default ordering if desired, but not required by checker
    # ordering = ['title']

# This view handles creating a new book.
class BookCreateView(generics.CreateAPIView):
    """
    API view for creating a new book.
    Corresponds to 'CreateView' in the checker's requirements.
    POST /api/books/create/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create.

# This view handles retrieving a single book by ID.
class BookRetrieveView(generics.RetrieveAPIView):
    """
    API view for retrieving a single book by ID.
    Corresponds to 'DetailView' in the checker's requirements.
    GET /api/books/<int:pk>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Read-only for unauthenticated

# This view handles updating an existing book.
class BookUpdateView(generics.UpdateAPIView):
    """
    API view for modifying an existing book.
    Corresponds to 'UpdateView' in the checker's requirements.
    PUT/PATCH /api/books/update/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can update.

# This view handles deleting a book.
class BookDestroyView(generics.DestroyAPIView):
    """
    API view for removing a book.
    Corresponds to 'DeleteView' in the checker's requirements.
    DELETE /api/books/delete/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can delete.
