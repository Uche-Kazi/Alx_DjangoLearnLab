# ~/Alx_DjangoLearnLab/django_blog/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login # Import login to automatically log in the user after registration
from django.contrib.auth.decorators import login_required # Import login_required decorator
from .forms import CustomUserCreationForm

def register_view(request):
    """
    View for user registration.
    Handles both displaying the registration form (GET) and processing form submission (POST).
    """
    if request.method == 'POST':
        # If the request is POST, it means the form was submitted.
        # Populate the form with data from the request.
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # If the form data is valid, save the new user.
            user = form.save()
            # Log the user in immediately after successful registration.
            login(request, user)
            # Redirect to a success page or the home page.
            return redirect('post_list') # Assuming 'post_list' is your blog homepage URL name
    else:
        # If the request is GET, display a blank registration form.
        form = CustomUserCreationForm()
    
    # Render the registration template, passing the form context.
    return render(request, 'registration/register.html', {'form': form})

@login_required # Ensures only logged-in users can access this view
def profile_view(request):
    """
    View for displaying the user's profile.
    This is a placeholder and will show a simple message for now.
    """
    return render(request, 'accounts/profile.html', {'user': request.user})

