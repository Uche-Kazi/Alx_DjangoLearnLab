# ~/Alx_DjangoLearnLab/django_blog/accounts/urls.py

# No longer needed if all accounts-related URLs are directly in django_blog/urls.py
# or moved to blog/urls.py.
# If you still have views specific to accounts that you want to include here,
# please specify them. For now, assuming it's empty or minimal.

# Example if you only keep 'logged_out' here (but it's already in django_blog/urls.py directly)
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('logged_out/', views.logged_out, name='logged_out'),
# ]

# As per the latest setup where 'logged_out' is handled directly in django_blog/urls.py,
# this file might be empty or removed. If you intend to use it, please provide the content.
# For now, I'll provide a minimal, correctly indented structure assuming there are still
# some unique account-related views you might want here.

from django.urls import path
from . import views

urlpatterns = [
    # If 'logged_out' is to be included here, it would look like this:
    # path('logged_out/', views.logged_out, name='logged_out'),

    # Add other account-specific URLs here if any remain that are not
    # handled by the blog app or the main django_blog urls.
    # For instance:
    # path('password_reset/', auth_views.PasswordResetView.as_view(...), name='password_reset'),
]
