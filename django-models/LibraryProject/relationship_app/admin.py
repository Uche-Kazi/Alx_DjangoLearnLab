# LibraryProject/relationship_app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Book, Loan, Author, Library, Librarian

# Register your models here.

# Admin configuration for UserProfile
class UserProfileInline(admin.StackedInline):
    """
    Inline for UserProfile to be displayed within the User admin page.
    This allows managing the UserProfile directly when editing a User.
    """
    model = UserProfile
    can_delete = False # Prevent deleting UserProfile directly from User admin
    verbose_name_plural = 'user profile' # Display name in the admin

class CustomUserAdmin(BaseUserAdmin):
    """
    Custom UserAdmin to include UserProfile inline.
    This replaces Django's default User admin to show the UserProfile.
    """
    inlines = (UserProfileInline,)
    # Customize the list display to show the user's role directly
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')

    def get_role(self, obj):
        """
        Custom method to display the UserProfile role in the admin list view.
        Checks if a user profile exists before trying to access its role.
        """
        return obj.userprofile.role if hasattr(obj, 'userprofile') else 'N/A'
    get_role.short_description = 'Role' # Column header for 'get_role'

# Re-register User model with the custom admin class
admin.site.unregister(User) # Unregister the default User admin
admin.site.register(User, CustomUserAdmin) # Register your custom User admin

# Register other models so they appear in the Django admin interface
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Library)
admin.site.register(Librarian)
