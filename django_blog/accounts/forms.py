# ~/Alx_DjangoLearnLab/django_blog/accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
# Import your custom user model
from .models import CustomUser

# Define a custom user registration form
# This form extends Django's built-in UserCreationForm
class UserRegisterForm(UserCreationForm):
    # Add an email field, making it required
    # Django's UserCreationForm only includes username and password by default
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'border p-2 rounded-lg w-full'}))

    class Meta(UserCreationForm.Meta):
        # Specify the model the form is for
        model = User
        # List the fields to be included in the form
        # 'email' is added here to ensure it's rendered by the form
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        """
        Custom validation for the email field.
        Ensures that the email provided is not already registered.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

# Define a custom user change form for use in the admin
# This form extends Django's built-in UserChangeForm
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        # Specify the custom user model this form is for
        model = CustomUser
        # List all the fields from your CustomUser model that you want to be editable in the admin
        # Importantly, ensure 'password' is NOT included here as UserChangeForm handles it separately
        # and including it here can cause issues with the admin password change functionality.
        fields = ('email', 'username', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    # If you need to include a 'password' field, you'd typically override __init__ or use
    # a separate form for password changes. For simplicity, we generally let the
    # default UserChangeForm's handling of password fields (which uses separate widgets)
    # work or omit it if you just want to edit other profile details.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure password related fields are handled correctly by the base UserChangeForm
        # or remove them if not desired for this specific profile update form.
        # Example: if you only want to edit email/username and not password, you might do:
        # if 'password' in self.fields:
        #    del self.fields['password']

