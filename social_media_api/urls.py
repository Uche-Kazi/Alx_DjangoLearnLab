from django.contrib import admin
from django.urls import path

# Import the new view from the same directory
from .views import hello_world_view  

urlpatterns = [
    # The default Django admin site
    path("admin/", admin.site.urls),
    
    # Existing API accounts path (currently empty, but you can add to it later)
    # path("api/accounts/", ),
    
    # This is the new path for the homepage (the empty string "" maps to the root URL)
    path("", hello_world_view),
]
