# ~/Alx_DjangoLearnLab/django_blog/blog/urls.py

from django.urls import path
from . import views # blog app's views
from accounts import views as accounts_views # Import accounts app's views
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

app_name = 'blog' # Define app_name for namespacing URLs

urlpatterns = [
    # Blog core views
    path('', views.home_page_view, name='home'), # Your simple homepage view

    # Authentication URLs (from accounts app, but pointed to from blog.urls)
    path('register/', accounts_views.register_view, name='register'),
    path('profile/', views.profile_edit_view, name='profile'), # <-- THIS LINE IS UPDATED
                                                              # Now points to profile_edit_view in blog.views
    # Django's built-in authentication views for login/logout
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name='logout'),
]
