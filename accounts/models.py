from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

<<<<<<< HEAD

# Create your models here.

class UserProfile(models.Model):
    # OneToOneField creates a link between this profile and a User instance.
    # The 'on_delete=models.CASCADE' means if the User is deleted, this profile is also deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# This signal is triggered every time a User object is saved.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # If a new User is created, also create a UserProfile for them.
    if created:
        UserProfile.objects.create(user=instance)
    # Save the existing UserProfile if the User is updated.
    instance.userprofile.save()
=======
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
>>>>>>> 1bbf6deb52f8e292397419e3b8a1dc2c44b8c68e
