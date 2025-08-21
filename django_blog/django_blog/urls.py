# ~/Alx_DjangoLearnLab/django_blog/django_blog/urls.py

from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views # Keep this for 'logged_out' if it's still outside blog app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')), # Now blog.urls will handle home, login, register, profile
    path('logged_out/', account_views.logged_out, name='logged_out'), # Keep if 'logged_out' is not in blog.urls
    # If there were other URLs in accounts.urls besides login/register/profile, you'd include them here under a different path,
    # but for now, we assume those are the main ones moved.
]
