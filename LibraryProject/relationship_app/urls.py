# LibraryProject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # This is the path for Django's built-in admin site.
    path('admin/', admin.site.urls),
    
    # This includes all the URL patterns from the 'relationship_app' module.
    # The empty string '' means that this app's URLs will be at the root of the
    # project (e.g., http://127.0.0.1:8000/register/).
    path('', include('LibraryProject.relationship_app.urls')),
]
