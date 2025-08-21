# ~/Alx_DjangoLearnLab/django_blog/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    """
    Custom Admin interface for CustomUser model.
    Inherits from Django's UserAdmin.
    """
    # Define the fields to be displayed in the list view of the admin
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        # Removed 'bio' from here, as it's no longer in the CustomUser model
    )

    # Define the fields to be used when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        # Add any custom fields here for the add user form if needed
        # (None, {'fields': ('bio',)}), # Example: if 'bio' were still in CustomUser
    )

    # Define the fields to be used when changing an existing user
    fieldsets = UserAdmin.fieldsets + (
        # Add any custom fields here for the change user form if needed
        # (None, {'fields': ('bio',)}), # Example: if 'bio' were still in CustomUser
    )

# Register your models with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile) # Register the Profile model
