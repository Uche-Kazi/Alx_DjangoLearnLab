from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
