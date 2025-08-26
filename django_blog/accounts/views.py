from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import CreateView # For class-based registration view
from django.urls import reverse_lazy

# Assuming you have a forms.py with a UserRegisterForm
from .forms import UserRegisterForm
from .models import Profile # Assuming you have a Profile model


class UserRegisterView(CreateView):
    form_class = UserRegisterForm # Use your custom registration form
    template_name = 'accounts/signup.html' # Create a signup.html template if you don't have one
    success_url = reverse_lazy('login') # Redirect to login page after successful registration

    def form_valid(self, form):
        response = super().form_valid(form)
        # You can add a message here if you wish
        messages.success(self.request, 'Your account has been created! You can now log in.')
        return response

@login_required
def profile(request, username):
    user_to_view = get_object_or_404(User, username=username)
    # Ensure the profile exists, or create a default one if necessary
    profile_obj, created = Profile.objects.get_or_create(user=user_to_view)

    context = {
        'user_to_view': user_to_view,
        'profile': profile_obj,
    }
    return render(request, 'accounts/profile.html', context)

# Don't forget any other views you have here
