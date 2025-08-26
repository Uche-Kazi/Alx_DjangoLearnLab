from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts' # This is crucial for namespacing your URLs

urlpatterns = [
    # Existing login and logout views
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    # New or updated signup view
    # Assuming you have a UserRegisterView in accounts/views.py
    path('signup/', views.UserRegisterView.as_view(), name='signup'),

    # Profile view
    path('profile/<str:username>/', views.profile, name='profile'),
]
