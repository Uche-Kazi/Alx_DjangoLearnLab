from django.contrib import admin
<<<<<<< HEAD
from .models import UserProfile

# Register your models here.

admin.site.register(UserProfile)
=======
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


# An inline admin for the UserProfile model
# This allows UserProfile fields to be edited directly on the User admin page.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


# Define a new User admin class
# This class inherits from the default Django User admin and adds our inline.
class CustomUserAdmin(DefaultUserAdmin):
    inlines = (UserProfileInline,)


# Re-register the default User model with our new CustomUserAdmin.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
>>>>>>> 1bbf6deb52f8e292397419e3b8a1dc2c44b8c68e
