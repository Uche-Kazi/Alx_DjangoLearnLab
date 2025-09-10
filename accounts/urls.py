from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserProfileAPIView

urlpatterns = [
    # URL for user registration. It points to the RegistrationAPIView.
    path('register/', RegistrationAPIView.as_view(), name='register'),
    
    # URL for user login. It points to the LoginAPIView.
    # This endpoint returns a token upon successful authentication.
    path('login/', LoginAPIView.as_view(), name='login'),
    
    # URL for user profile management.
    # This route is used to view and update the user's profile.
    # It requires authentication, as handled by the UserProfileAPIView.
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
]
