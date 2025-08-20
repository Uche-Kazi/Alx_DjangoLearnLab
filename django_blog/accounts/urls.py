# ~/Alx_DjangoLearnLab/django_blog/accounts/urls.py

from django.urls import path
from . import views # Import views from the current app

urlpatterns = [
    # URL for user registration.
    # Maps '/register/' to the register_view function.
    # The 'name' 'register' can be used for reverse lookups (e.g., in templates).
    path('register/', views.register_view, name='register'),
    
    # URL for user profile management.
    # Maps '/profile/' to the profile_view function.
    # The 'name' 'profile' can be used for reverse lookups.
    path('profile/', views.profile_view, name='profile'),
]
