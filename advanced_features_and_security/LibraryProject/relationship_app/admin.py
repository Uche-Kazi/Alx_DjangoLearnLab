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

# Custom Admin for CustomUser to display the role field and new custom fields
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    # Add 'role' and new custom fields to the fieldsets for viewing/editing existing users
    fieldsets = BaseUserAdmin.fieldsets + (
        (('Custom Fields', {'fields': ('role', 'date_of_birth', 'profile_photo',)}),) # Added date_of_birth and profile_photo
    )
    # Add 'role' and new custom fields to the add_fieldsets for adding new users
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (('Custom Fields', {'fields': ('role', 'date_of_birth', 'profile_photo',)}),) # Added date_of_birth and profile_photo
    )
    # Add 'role' and date_of_birth to the list display in the admin change list page
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role', 'date_of_birth') # Added date_of_birth
    # You might also want to add list_filter or search_fields if needed for these new fields

