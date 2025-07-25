from django.urls import path, include
# Import all views needed for URL patterns from your app using 'from . import views'
# This allows us to refer to views like views.RegisterView
from . import views
# Import Django's built-in authentication views directly
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy # Needed for reverse_lazy

app_name = 'relationship_app' # Namespace for this app's URLs

urlpatterns = [
    # Existing URL patterns
    path('books/', views.list_books, name='book_list'), # Refer to list_books via views.
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'), # Refer to LibraryDetailView via views.

    # New Authentication URL patterns
    # CRITICAL FIX: Use .as_view() for the class-based RegisterView
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Using Django's built-in LoginView directly with template_name
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # Using Django's built-in LogoutView directly with template_name
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html', next_page=reverse_lazy('relationship_app:login')), name='logout'),
]
