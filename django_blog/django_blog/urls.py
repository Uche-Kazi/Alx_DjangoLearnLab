# django_blog/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site URLs
    path('admin/', admin.site.urls),

    # Allauth URLs for authentication (login, logout, signup, etc.)
    path('accounts/', include('allauth.urls')),

    # Blog application URLs:
    # This line now exclusively handles routing for your blog app,
    # making the blog post list accessible at the root URL (http://127.0.0.1:8000/).
    # The 'namespace='blog' is defined here once.
    path('', include('blog.urls', namespace='blog')),
]
