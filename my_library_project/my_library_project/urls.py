# my_library_project/my_library_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView # For redirecting root URL to book list
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the bookshelf app URLs
    path('', include('bookshelf.urls')),
    
    # CRITICAL FIX: Add Django's built-in authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Redirect to home after logout
]
