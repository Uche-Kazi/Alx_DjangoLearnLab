from django.urls import path
# Import all views needed for URL patterns
# CRITICAL FIX: Changed import for logout view
from .views import list_books, LibraryDetailView, RegisterView, CustomLoginView, custom_logout_view

app_name = 'relationship_app' # Namespace for this app's URLs

urlpatterns = [
    # Existing URL patterns
    path('books/', list_books, name='book_list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # New Authentication URL patterns
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # CRITICAL FIX: Changed to use the function-based custom_logout_view
    path('logout/', custom_logout_view, name='logout'),
]
