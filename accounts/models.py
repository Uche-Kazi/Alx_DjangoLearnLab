from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    A model to store additional information about a user.
    """
    # Use a OneToOneField to link a user to their profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Optional text field for a user's biography.
    bio = models.TextField(max_length=500, blank=True)
    
    # Optional image field for a user's profile picture.
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a UserProfile for every new User.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the UserProfile when the User is saved.
    """
    instance.profile.save()
