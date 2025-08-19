# ~/Alx_DjangoLearnLab/django_blog/blog/admin.py

from django.contrib import admin
from .models import Post # Import your Post model

# Register your models here.
admin.site.register(Post)
