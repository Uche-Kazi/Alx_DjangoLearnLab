from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),
    
    # Include the URL patterns from the accounts app under the /api/accounts/ path
    path('api/accounts/', include('accounts.urls')),
]
