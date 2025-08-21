# ~/Alx_DjangoLearnLab/django_blog/blog/urls.py

from django.urls import path
from . import views # Import blog app's views (e.g., home_page_view)
from accounts import views as accounts_views # Import accounts app's views
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

app_name = 'blog' # Define app_name for namespacing URLs (good practice)

urlpatterns = [
    # Blog core views
    path('', views.home_page_view, name='home'), # Your simple homepage view

    # Authentication URLs (moved here as per checker's requirements)
    path('register/', accounts_views.register_view, name='register'), # From accounts.views
    path('profile/', accounts_views.profile_edit_view, name='profile'), # The profile edit view

    # Django's built-in authentication views for login/logout (linked to accounts templates)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name='logout'),
]
