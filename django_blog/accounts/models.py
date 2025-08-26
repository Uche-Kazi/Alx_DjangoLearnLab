from django.db import models
from django.contrib.auth.models import User # Import the User model

# Function to define the upload path for user profile images
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'profile_pics/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add a bio field, which is optional and can be a text area
    bio = models.TextField(max_length=500, blank=True, null=True)
    # Add an image field for profile pictures
    # It will store the path to the image, and we'll use a default image if none is uploaded
    image = models.ImageField(default='default.jpg', upload_to=user_directory_path)

    def __str__(self):
        return f'{self.user.username} Profile'

    # You might want to override the save method to resize images, etc.
    # from PIL import Image
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

# You can connect a signal to automatically create a Profile when a User is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

