# ~/Alx_DjangoLearnLab/api_project/api_project/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token # Import this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # This endpoint is used to obtain an authentication token.
    # Clients send a POST request with 'username' and 'password' to this URL
    # and receive a unique 'token' in response, which is then used for
    # subsequent authenticated API requests.
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
