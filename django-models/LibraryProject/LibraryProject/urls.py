# LibraryProject/LibraryProject/urls.py

from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth import views as auth_views # This import is no longer needed if app handles auth URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the URLs from your relationship_app
    path('', include('LibraryProject.relationship_app.urls')), # This makes your app's home page the project's root

    # REMOVE THESE LINES (or ensure they point to your app's views if you prefer project-level auth URLs)
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    # path('register/', auth_views.LoginView.as_view(template_name='registration/register.html'), name='register'),
]
