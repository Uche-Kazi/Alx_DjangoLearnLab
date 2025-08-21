# ~/Alx_DjangoLearnLab/django_blog/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Corrected import: change SignUpForm to UserRegisterForm
from .forms import UserRegisterForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm # Also update this line
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',] # Adjust fields as needed for admin list display

# Register your CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
