from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Custom User Registration Form
# We inherit from Django's built-in UserCreationForm to easily create new users.
# This form handles the username, password, and password confirmation fields.
class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Specify the model to use for creating users (Django's default User model).
        model = UserCreationForm.Meta.model
        # Specify the fields that will be included in the registration form.
        # 'username' and 'password' are handled by UserCreationForm itself,
        # but you can add more fields here if your User model has them.
        fields = UserCreationForm.Meta.fields + ('email',) # Example: Adding email field
