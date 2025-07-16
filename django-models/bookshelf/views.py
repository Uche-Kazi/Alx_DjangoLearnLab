from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Define the SignUpView for user registration
class SignUpView(CreateView):
    # Use Django's built-in UserCreationForm for handling user registration fields.
    form_class = UserCreationForm
    # Redirect to the 'login' URL name upon successful registration.
    success_url = reverse_lazy("login")
    # Specify the template to render for the signup form.
    template_name = "registration/signup.html"

# You can keep or remove the default index view if you have one,
# or add other views here as needed for your bookshelf app.
# For now, we're just adding the SignUpView.