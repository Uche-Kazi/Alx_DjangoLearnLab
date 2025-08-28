# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# This is a very basic profile view.
# We'll enhance this later with forms for updating profile and user data.
@login_required
def profile(request):
    """
    Renders the user's profile page.
    Requires the user to be logged in.
    """
    return render(request, 'accounts/profile.html')

# If you have other views in accounts/views.py, keep them as is.
# Example for registration (if you have one):
# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'
