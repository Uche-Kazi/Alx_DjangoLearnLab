# ~/Alx_DjangoLearnLab/django_blog/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Import Django's default UserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define an inline admin descriptor for Profile model
# This allows Profile model to be edited on the User admin page
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,) # Add the ProfileInline here

# Re-register UserAdmin
admin.site.unregister(User) # Unregister the default User admin
admin.site.register(User, UserAdmin) # Register our custom UserAdmin
