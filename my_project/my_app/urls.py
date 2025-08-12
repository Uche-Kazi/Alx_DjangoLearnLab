# ~/Alx_DjangoLearnLab/my_project/my_app/urls.py

from django.urls import path
from .views import BookListCreateAPIView # Import your API view

urlpatterns = [
    # Defines the URL for the book API endpoint.
    # When accessed at `api/books`, it will use BookListCreateAPIView.
    path("api/books/", BookListCreateAPIView.as_view(), name="book_list_create"),
]
