# ~/Alx_DjangoLearnLab/api_project/api/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated # Import IsAuthenticated

from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    Provides full CRUD operations (list, create, retrieve, update, destroy).

    Authentication and Permissions:
    - queryset: Retrieves all Book objects from the database.
    - serializer_class: Uses BookSerializer for data serialization and deserialization.
    - permission_classes:
        - [IsAuthenticated]: This permission class ensures that only authenticated
          users (i.e., users who provide a valid authentication token) can
          access and perform any operations (GET, POST, PUT, DELETE) on these
          API endpoints. Unauthenticated requests will receive a 401 Unauthorized response.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Enforce authentication for all operations

