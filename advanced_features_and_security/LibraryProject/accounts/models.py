from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager to handle user and superuser creation.
    We are inheriting from BaseUserManager because our CustomUser model
    will be a proxy of AbstractUser, not a complete replacement.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        The email field is used as the unique identifier.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        Superusers are required to have all permissions.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Custom user model that extends AbstractUser.
    We will use the 'email' field as the unique identifier for authentication
    instead of the default 'username'.
    """
    # The default username field is already provided by AbstractUser,
    # but we are making 'email' the unique identifier for auth.
    email = models.EmailField(unique=True)

    # Add the custom fields required by the task description
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # Replace the username with email for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Use the custom manager
    objects = CustomUserManager()

    def __str__(self):
        """
        Returns a string representation of the user.
        """
        return self.email
