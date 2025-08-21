# ~/Alx_DjangoLearnLab/django_blog/accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model # Use get_user_model to get the active user model

# Get the CustomUser model defined in accounts/models.py
CustomUser = get_user_model()

# This form is for user registration (used by register_view)
class RegisterForm(UserCreationForm):
    # Adding email as a required field for registration
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'border p-2 rounded-lg w-full'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser # Ensure this uses CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists, excluding the current user's email if it's an update scenario
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

# This form is for updating the User model's fields (username, email, etc.)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'border p-2 rounded-lg w-full'}))
    username = forms.CharField(max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'border p-2 rounded-lg w-full'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email'] # Fields that users can update about themselves

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Ensure email is unique, excluding the current user's email if it's an update
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already registered by another user.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Ensure username is unique, excluding the current user's username if it's an update
        if CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

# This form is for updating additional profile-specific fields (like bio, image, etc.)
# You need to define a Profile model in accounts/models.py if you haven't already.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        # Assuming you have a Profile model linked to CustomUser
        # You'll need to define it in accounts/models.py
        model = CustomUser # For now, we'll use CustomUser directly for simplicity if no separate Profile model is created.
        # If you have a separate Profile model, change `model = CustomUser` to `model = Profile`
        # and ensure Profile has fields like 'bio', 'image', 'location'
        # e.g., model = Profile
        fields = ['first_name', 'last_name'] # Using fields directly from CustomUser for demonstration
                                            # If you have a separate Profile model, these would be its fields.
                                            # e.g., fields = ['bio', 'image', 'location']
