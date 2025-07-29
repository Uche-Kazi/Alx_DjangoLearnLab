# LibraryProject/relationship_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser # Import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser # Use CustomUser
        # Include 'role' and other fields you might want to capture on registration
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'role',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser # Use CustomUser
        fields = UserChangeForm.Meta.fields

class UserRoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = CustomUser # Use CustomUser for role assignment
        fields = ['role']
