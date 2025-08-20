# ~/Alx_DjangoLearnLab/django_blog/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login # Import login to automatically log in the user after registration
from django.contrib.auth.decorators import login_required # Import decorator for login required
from .forms import CustomUserCreationForm, CustomUserChangeForm # Import both forms

def register_view(request):
    """
    View for user registration.
    Handles both displaying the registration form (GET) and processing form submission (POST).
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list') # Redirect to the blog homepage URL name
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required # Ensures only logged-in users can access this view
def profile_view(request):
    """
    View for user profile management.
    Allows authenticated users to view and update their profile details.
    """
    if request.method == 'POST':
        # When updating a user, pass request.FILES for profile_photo uploads
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Add a success message here later if you implement Django Messages
            return redirect('profile') # Redirect back to the profile page to see updates
    else:
        # For GET requests, pre-fill the form with the current user's data
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form, 'user': request.user})

