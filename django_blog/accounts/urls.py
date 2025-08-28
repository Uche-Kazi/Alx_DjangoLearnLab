# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts' # This is good practice for namespacing URLs

urlpatterns = [
    # ... other account-related URLs if you have any ...
    path('profile/', views.profile, name='profile'),
]
