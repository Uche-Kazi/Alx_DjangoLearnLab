# ~/Alx_DjangoLearnLab/django_blog/django_blog/urls.py

from django.contrib import admin
from django.urls import path, include # Ensure 'include' is imported
# Import Django's built-in authentication views. We'll alias them as auth_views.
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the URLs from your 'blog' app.
    path('', include('blog.urls')),
    # Include the URLs from your 'accounts' app under the 'accounts/' prefix.
    path('accounts/', include('accounts.urls')), # This already includes 'register/'

    # Add Django's built-in login and logout views directly here for simplicity
    # Login view: Uses Django's LoginView with a custom template.
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Logout view: Uses Django's LogoutView. next_page specifies where to redirect after logout.
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

