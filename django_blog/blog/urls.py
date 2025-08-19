# ~/Alx_DjangoLearnLab/django_blog/blog/urls.py

from django.urls import path
from . import views # Import views from the current app

urlpatterns = [
    # URL for displaying a list of all blog posts
    # Name 'post_list' will be used for reverse lookups (e.g., in templates)
    path('', views.post_list, name='post_list'),
    
    # URL for displaying details of a single blog post
    # <int:pk> captures the primary key from the URL and passes it to the view
    # Name 'post_detail' will be used for reverse lookups
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]

