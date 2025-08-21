# ~/Alx_DjangoLearnLab/django_blog/blog/views.py

from django.shortcuts import render, redirect
from django.contrib import messages # Needed for messages framework
from django.contrib.auth.decorators import login_required # Needed for @login_required

# Import forms and models from accounts app
# Adjust these imports based on your actual forms and models
from accounts.forms import UserUpdateForm, ProfileUpdateForm
from accounts.models import CustomUser # Or just Profile if ProfileUpdateForm works with it

def home_page_view(request):
    """
    Simple placeholder view for the blog homepage.
    """
    return render(request, 'blog/home.html', {})

@login_required
def profile_edit_view(request):
    """
    Allows authenticated users to view and edit their profile details.
    Handles GET (display form) and POST (update user information) requests.
    """
    # Ensure a Profile object exists for the user.
    # This assumes you have a Profile model with a OneToOneField to CustomUser.
    # If you don't have a separate Profile model, adjust this logic.
    if not hasattr(request.user, 'profile'):
        from accounts.models import Profile # Local import to avoid circular dependency
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        # Instantiate forms with POST data and current user/profile instance
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES, # For profile pictures
                                         instance=request.user.profile) # Pass instance of profile

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile') # Redirect back to the profile page (name 'profile' in blog/urls.py)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Instantiate forms with current user/profile data for GET request
        user_form = UserUpdateForm(instance=request.user)
        if hasattr(request.user, 'profile'):
            profile_form = ProfileUpdateForm(instance=request.user.profile)
        else:
            # Should not happen if previous check creates it, but as fallback
            profile_form = ProfileUpdateForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile_edit.html', context) # Assuming you have this template
