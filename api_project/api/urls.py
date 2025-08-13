# ~/Alx_DjangoLearnLab/api_project/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter # Import DefaultRouter
from .views import BookViewSet # Import your BookViewSet

# Create a router instance
router = DefaultRouter()
# Register the BookViewSet with the router.
# The 'books_all' prefix will be used for the URLs (e.g., /api/books_all/)
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Include all routes registered with the router.
    # This automatically generates URLs for list, create, retrieve, update, delete operations.
    path('', include(router.urls)),
]
