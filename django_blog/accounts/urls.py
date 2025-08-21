# ~/Alx_DjangoLearnLab/django_blog/accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views # Import Django's built-in auth views
from . import views # Import views from the current app (for signup and profile)

urlpatterns = [
    # URL for user registration
    path('signup/', views.signup, name='signup'),
    # URL for user login using Django's built-in LoginView
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # URL for user logout using Django's built-in LogoutView
    # It will redirect to the URL named 'logged_out' after successful logout
    path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name='logout'),
    # URL for the user profile page (requires login)
    path('profile/', views.profile, name='profile'),
]
