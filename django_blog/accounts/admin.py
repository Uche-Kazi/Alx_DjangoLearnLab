# ~/Alx_DjangoLearnLab/django_blog/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your CustomUser model with the admin site.
# We use UserAdmin for CustomUser to get all the default user management features.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Customizes the appearance and behavior of the CustomUser model in the admin.
    We inherit from the default UserAdmin to keep all the default functionality,
    but we will add our custom fields to the fieldsets and list_display.
    """
    # The fields to display in the list view of the admin panel.
    list_display = (
        'username', # Keep username here for display if you want it
        'email',
        'first_name',
        'last_name',
        'is_staff',
        # 'date_of_birth', # Uncomment if you want this in the list display
    )
    
    # Define the fieldsets for the change form.
    # We include all the standard fields and a new fieldset for our custom fields.
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('date_of_birth', 'profile_photo')}),
    )

    # Define the fieldsets for the add form (creating a new user).
    # We'll use the same structure as the change form.
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'username', 'date_of_birth', 'profile_photo')}), # Include email and username for creation
    )

    # Ensure email is used as the username field in the admin forms
    # ordering = ('email',) # Uncomment if you want to order by email by default

# No need to call admin.site.register(CustomUser, CustomUserAdmin) explicitly
# because @admin.register(CustomUser) handles it.
