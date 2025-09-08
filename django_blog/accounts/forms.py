from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile # Assuming you have a Profile model

class UserRegisterForm(UserCreationForm):
    # Add any extra fields if needed, or customize existing ones
    email = forms.EmailField() # Example: making email mandatory

    class Meta:
        model = User
        fields = ['username', 'email', 'password'] # Specify fields for registration

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image'] # Example fields for a user profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
