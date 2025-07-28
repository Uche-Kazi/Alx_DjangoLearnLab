# LibraryProject/relationship_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile # Import UserProfile

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration.
    Extends Django's UserCreationForm.
    """
    email = forms.EmailField(required=False, help_text="Optional: Enter a valid email address.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class UserRoleAssignmentForm(forms.ModelForm):
    """
    Form for assigning roles to existing users in the admin interface.
    """
    class Meta:
        model = UserProfile
        fields = ['role'] # Only allow changing the role

