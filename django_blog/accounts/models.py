# ~/Alx_DjangoLearnLab/django_blog/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image # Pillow library for image processing

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Add any additional fields here if needed for the user directly.
    """
    # Example of an additional field, though not strictly required for this task
    # bio = models.TextField(max_length=500, blank=True)
    pass # No extra fields added for CustomUser for now, using default fields

    def __str__(self):
        return self.username

class Profile(models.Model):
    """
    Profile model to store additional user information,
    related to CustomUser with a OneToOne relationship.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        """
        String representation of the Profile object.
        """
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Override the save method to resize profile images.
        """
        super().save(*args, **kwargs) # Call the original save method first

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) # Save the resized image back to the same path
