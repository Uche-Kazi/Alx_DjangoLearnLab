# ~/Alx_DjangoLearnLab/api_project/api/urls.py

from django.urls import path
from .views import BookList # Import your BookList API view

urlpatterns = [
    # Maps the 'books/' path to the BookList view.
    # The 'name' argument is used for reverse lookups.
    path('books/', BookList.as_view(), name='book-list'),
]
