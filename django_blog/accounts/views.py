# ~/Alx_DjangoLearnLab/django_blog/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm # Assuming these are defined in forms.py
from django.contrib import messages

# It's good practice to import built-in views like LoginView directly if used
from django.contrib.auth.views import LoginView, LogoutView

# Custom Login View (if you still want to use it instead of Django's default)
# If you're using Django's built-in LoginView directly in blog/urls.py,
# you might not need this custom login_view function.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('blog:home') # Redirect to blog home after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Custom Logout View (if you still want to use it)
# Similar to login, you might use Django's built-in LogoutView directly.
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('logged_out') # Redirect to a simple logged out page

# Custom registration view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # You might want to automatically log in the user after registration
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('blog:home') # Redirect to blog home after registration
        else:
            messages.error(request, "Error creating account. Please check your input.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# This is the simplified logged_out view as requested earlier
def logged_out(request):
    return render(request, 'accounts/logged_out.html')

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # Check if request.user has an associated profile, create one if not
        if not hasattr(request.user, 'profile'):
            from .models import Profile # Import Profile model here to avoid circular dependency
            Profile.objects.create(user=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('blog:profile') # Redirect to the user's profile page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        # Handle case where user might not have a profile yet (e.g., old users or direct creation)
        if hasattr(request.user, 'profile'):
            profile_form = ProfileUpdateForm(instance=request.user.profile)
        else:
            # Create a new, empty profile form if no profile exists
            profile_form = ProfileUpdateForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile_edit.html', context)

# Add this placeholder view if you moved profile display here
# or adjust it to be called from blog.views if it's there
@login_required
def profile_view(request):
    # This view would typically fetch and display user and profile data
    # If blog.views handles this, you might not need it here.
    return render(request, 'accounts/profile.html') # Or wherever your profile template is
