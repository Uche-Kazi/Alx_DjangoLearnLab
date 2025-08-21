# ~/Alx_DjangoLearnLab/django_blog/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you want for your user model here.
    # For example:
    # age = models.IntegerField(null=True, blank=True)

    # These fields are now active on your CustomUser model:
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
