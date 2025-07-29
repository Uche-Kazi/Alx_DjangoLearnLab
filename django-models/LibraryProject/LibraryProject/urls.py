# LibraryProject/LibraryProject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403 # Import handler403

# Import your custom 403 handler view
# Ensure this import path is correct for your project structure
from LibraryProject.relationship_app import views as relationship_app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('LibraryProject.relationship_app.urls')), # This makes your app's home page the project's root
]

# Define custom error handlers
# This tells Django to use custom_403_view from your app for 403 errors
handler403 = relationship_app_views.custom_403_view
