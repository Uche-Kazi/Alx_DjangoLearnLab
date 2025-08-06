# my_library_project/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your CustomUser model with the admin site.
# We use UserAdmin for CustomUser to get all the default user management features.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the user list in the admin
    list_display = ('email', 'username', 'is_staff', 'is_active')
    # Define fields for adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'date_of_birth', 'profile_photo')}),
    )
    # Define fields for editing an existing user
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    # Ensure email is used as the username field in the admin forms
    ordering = ('email',)

