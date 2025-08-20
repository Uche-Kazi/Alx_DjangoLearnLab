# ~/Alx_DjangoLearnLab/django_blog/accounts/forms.py

from django import forms
# Import UserCreationForm and get_user_model from Django's authentication system
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # Import UserChangeForm
from django.contrib.auth import get_user_model

# Get your CustomUser model
CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users.
    It extends Django's built-in UserCreationForm to work with our CustomUser model.
    """
    class Meta(UserCreationForm.Meta):
        # Specify the custom user model this form is for
        model = CustomUser
        # Define the fields that will appear on the registration form.
        # Ensure 'email' and 'username' are included as per your CustomUser definition.
        fields = ('email', 'username',) # 'password' and 'password2' are handled by UserCreationForm implicitly

class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating existing users.
    It extends Django's built-in UserChangeForm and works with our CustomUser model.
    """
    class Meta:
        model = CustomUser
        # Define the fields that will appear on the profile edit form.
        # Include custom fields like 'date_of_birth' and 'profile_photo'.
        # We also need to include 'username' and 'email'.
        fields = ('email', 'username', 'date_of_birth', 'profile_photo',)

