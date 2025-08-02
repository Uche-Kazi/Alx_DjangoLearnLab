from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Customizes the appearance and behavior of the CustomUser model in the admin.
    We inherit from the default UserAdmin to keep all the default functionality,
    but we will add our custom fields to the fieldsets and list_display.
    """
    # The fields to display in the list view of the admin panel.
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'date_of_birth',
    )
    
    # Define the fieldsets for the change form.
    # We include all the standard fields and a new fieldset for our custom fields.
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # Define the fieldsets for the add form (creating a new user).
    # We'll use the same structure as the change form.
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Unregister the default User model if it was ever registered
# This prevents potential conflicts with our custom user model.
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass

# Register the CustomUser model with our custom Admin class.
admin.site.register(CustomUser, CustomUserAdmin)
