from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include app URLs if needed, but for this task, usually not
    # path('relationship_app/', include('LibraryProject.LibraryProject.relationship_app.urls')),
]
