# ~/Alx_DjangoLearnLab/django_blog/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields you want for your user model here.
    # For example:
    # age = models.IntegerField(null=True, blank=True)
    # bio = models.TextField(max_length=500, blank=True)
    
    # You can add a profile picture field too, if needed
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    pass

    def __str__(self):
        return self.username

