# ~/Alx_DjangoLearnLab/django_blog/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import views as auth_views # No longer needed here for LoginView/LogoutView
from .forms import UserRegisterForm

def signup(request):
    """
    Handles user registration.
    If the request method is POST, it processes the form submission.
    If the form is valid, it saves the user, displays a success message,
    and redirects to the login page.
    Otherwise, it displays the empty registration form.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # Redirect to the login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required # This decorator ensures only logged-in users can access this view
def profile(request):
    """
    Renders the user profile page.
    This view requires the user to be authenticated.
    """
    return render(request, 'accounts/profile.html')

# Django's built-in Login View and Logout View are now handled directly in urls.py
# So, we remove:
# user_login = auth_views.LoginView.as_view(template_name='accounts/login.html')
# user_logout = auth_views.LogoutView.as_view(next_page='logged_out')

def logged_out(request):
    """
    Renders a simple page indicating the user has been logged out.
    """
    messages.info(request, "You have been logged out.")
    return render(request, 'accounts/logged_out.html')
