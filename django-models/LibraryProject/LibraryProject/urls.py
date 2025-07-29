# LibraryProject/LibraryProject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403 # Import handler403

# Correct import path for your custom 403 handler view
from LibraryProject.relationship_app import views as relationship_app_views # <-- CORRECTED THIS LINE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('LibraryProject.relationship_app.urls')), # This makes your app's home page the project's root
]

# Define custom error handlers
handler403 = relationship_app_views.custom_403_view # Point to a view in your app
