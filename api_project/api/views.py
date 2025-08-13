# ~/Alx_DjangoLearnLab/api_project/api/views.py

from rest_framework import viewsets # Import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    Provides full CRUD operations (list, create, retrieve, update, destroy).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Note: The previous BookList view is removed as BookViewSet handles listing.
