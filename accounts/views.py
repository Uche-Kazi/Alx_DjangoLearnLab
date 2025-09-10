from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer

# Get the active User model
User = get_user_model()

class RegistrationAPIView(generics.CreateAPIView):
    # This view allows users to register.
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

class LoginAPIView(generics.GenericAPIView):
    # This view allows registered users to log in and get a token.
    serializer_class = LoginSerializer

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating the authenticated user's profile.
    - GET request: Fetches the profile of the currently logged-in user.
    - PUT/PATCH request: Updates the profile of the currently logged-in user.
    """
    # Only authenticated users can access this view
    permission_classes = [IsAuthenticated]
    # Use the UserSerializer to handle the data
    serializer_class = UserSerializer
    # Define the queryset, which is the set of all User objects
    queryset = User.objects.all()

    def get_object(self):
        """
        Overrides the default get_object method to return the authenticated user's profile.
        This ensures a user can only view or update their own data.
        """
        return self.request.user
