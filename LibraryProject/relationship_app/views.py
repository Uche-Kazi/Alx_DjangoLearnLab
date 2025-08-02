# relationship_app/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# This view will display the homepage.
def home(request):
    """
    Renders the main homepage.
    """
    return render(request, 'home.html')

# This view will handle user registration.
def register(request):
    """
    Placeholder view for user registration.
    Will render a form and handle form submission.
    """
    return render(request, 'register.html')

# This view will handle user login.
def login_view(request):
    """
    Placeholder view for user login.
    Will render a login form and handle authentication.
    """
    return render(request, 'login.html')

# This is a protected view that requires the user to be logged in.
@login_required(login_url='relationship_app:login')
def dashboard(request):
    """
    Placeholder view for the user's dashboard.
    Accessible only to logged-in users.
    """
    return render(request, 'dashboard.html')

# This view handles user logout.
def logout_view(request):
    """
    Logs out the current user and redirects to the home page.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('relationship_app:home')
