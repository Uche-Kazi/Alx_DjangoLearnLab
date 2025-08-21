# ~/Alx_DjangoLearnLab/django_blog/django_blog/urls.py

from django.contrib import admin
from django.urls import path, include # Make sure 'include' is imported
from accounts import views as account_views # Import account views for logout redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')), # Include URLs from your blog app
    path('accounts/', include('accounts.urls')), # Include URLs from your accounts app
    path('logged_out/', account_views.logged_out, name='logged_out'), # Define the logged_out URL here
]
