# LibraryProject/relationship_app/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile # Import your UserProfile model

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a UserProfile when a new User is created.
    If a User is updated, it ensures their UserProfile is also saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
    # This ensures the UserProfile is updated if the User is saved again
    # (e.g., if you change user fields in admin and want profile to reflect changes)
    # It also handles cases where a superuser might not have a profile initially.
    instance.userprofile.save()
