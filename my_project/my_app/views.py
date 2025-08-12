# ~/Alx_DjangoLearnLab/my_project/my_app/views.py

from rest_framework import generics
from .models import Book # Import your Book model
from .serializers import BookSerializer # Import your BookSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all books or create a new book.
    - Lists all Book objects from the database.
    - Uses BookSerializer for data serialization and deserialization.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

