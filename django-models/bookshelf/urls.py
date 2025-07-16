# bookshelf/urls.py (This file MUST be inside the 'bookshelf' app folder)
from django.urls import path
from . import views # Import views from the current app

urlpatterns = [
    # Define the URL path for the signup view.
    # When a user navigates to /bookshelf/signup/, the SignUpView will be rendered.
    path("signup/", views.SignUpView.as_view(), name="signup"),
    # Add other URL patterns for your bookshelf app here if needed in the future.
]