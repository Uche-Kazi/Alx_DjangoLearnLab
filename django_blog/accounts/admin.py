# ~/Alx_DjangoLearnLab/django_blog/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Ensure your add_fieldsets and fieldsets are correctly defined without duplicates
    # and include 'bio' if you want it editable.
    # ... (your add_fieldsets and fieldsets here, as discussed in previous steps) ...

    # This is the critical part for the current error:
    list_display = UserAdmin.list_display + ('bio',) # <--- Ensure 'bio' is exactly here
    # You could also explicitly list all fields:
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'bio')
    # Make sure 'bio' is spelled correctly and matches the field name in models.py

    # Any other admin configurations...
    search_fields = ('username', 'email', 'bio',)
    ordering = ('username',)
