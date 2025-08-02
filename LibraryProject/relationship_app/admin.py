# advanced_features_and_security/relationship_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book, Author, Loan

# Register your models here.

# Customize the User model in the admin panel
class CustomUserAdmin(UserAdmin):
    # Specify the fields to display in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    
    # Specify the fields for filtering the list
    list_filter = ('is_staff', 'is_active', 'role')

    # Add the 'role' field to the detail view's fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Register the CustomUser model with the customized admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register the other models with the default admin interface
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Loan)
