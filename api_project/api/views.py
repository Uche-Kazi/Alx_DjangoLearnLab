# ~/Alx_DjangoLearnLab/api_project/api/views.py

from rest_framework import generics
from .models import Book # Import your Book model
from .serializers import BookSerializer # Import your BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to list all books.
    - Retrieves all Book objects from the database.
    - Uses BookSerializer to convert Book instances into JSON format.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

