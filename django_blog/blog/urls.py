# ~/Alx_DjangoLearnLab/django_blog/blog/urls.py

from django.urls import path
from . import views # Import views from the current app

urlpatterns = [
    path('', views.home_page_view, name='home'), # Example: a homepage view
    # Add other blog-related URLs here (e.g., post detail, new post, etc.)
]
