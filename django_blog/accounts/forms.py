# ~/Alx_DjangoLearnLab/django_blog/accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users.
    It extends Django's built-in UserCreationForm to work with our CustomUser model.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username',) # 'password' and 'password2' are handled by UserCreationForm implicitly

    def __init__(self, *args, **kwargs):
        """
        Constructor to add Tailwind CSS classes to form widgets.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Add common Tailwind classes for input fields
            field.widget.attrs.update({
                'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-blue-500 rounded-md',
                'placeholder': field.label # Use label as placeholder
            })
            # Specifically handle password fields for better UI
            if field_name in ['password', 'password2']: # UserCreationForm fields
                field.widget.attrs['placeholder'] = '********'
            if field_name == 'email':
                field.widget.attrs['type'] = 'email' # Ensure email input type
