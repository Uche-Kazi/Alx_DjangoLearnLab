# LibraryProject/relationship_app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Author, Book, Library, Librarian, Loan, CustomUser # Import CustomUser

# Register your other models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(Loan)

# Custom Admin for CustomUser to display the role field
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # Add 'role' to the fieldsets for both viewing/editing and adding new users
    fieldsets = BaseUserAdmin.fieldsets + (
        (('Roles', {'fields': ('role',)}),)
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (('Roles', {'fields': ('role',)}),)
    )
    # Add 'role' to the list display in the admin change list page
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
