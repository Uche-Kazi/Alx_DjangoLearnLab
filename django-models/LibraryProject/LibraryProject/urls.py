"""
URL configuration for LibraryProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # Ensure 'include' is imported

# CRITICAL FIX: Import custom_logout_view instead of CustomLogoutView
from LibraryProject.relationship_app.views import RegisterView, CustomLoginView, custom_logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library_app/', include('LibraryProject.relationship_app.urls')), # This includes your existing app URLs

    # Add the authentication URLs directly here
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # CRITICAL FIX: Use the function-based view directly
    path('logout/', custom_logout_view, name='logout'),
]
