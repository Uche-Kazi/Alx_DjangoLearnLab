# LibraryProject/LibraryProject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403 # Import handler403

# Import your custom 403 handler view
# Ensure this import path is correct for your project structure
from LibraryProject.relationship_app import views as relationship_app_views
from django.views.generic import TemplateView # For a simple 403 handler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # ADD THIS LINE for Django's authentication URLs
    path('', include('LibraryProject.relationship_app.urls')), # This makes your app's home page the project's root
]

# Define custom error handlers
# This tells Django to use custom_403_view from your app for 403 errors
# Temporarily pointing to a generic template view for 403 if custom_403_view is not yet defined
# We will define a proper custom_403_view in relationship_app/views.py next.
handler403 = relationship_app_views.error_page # Assuming error_page can serve as a generic 403 handler for now
