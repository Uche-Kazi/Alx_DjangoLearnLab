# ~/Alx_DjangoLearnLab/django_blog/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager to handle user and superuser creation.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
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
    """
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # CRITICAL FIX: Add unique related_name arguments to avoid clashes with the default User model.
    # This is necessary because AbstractUser defines these, and if you have other apps
    # that might implicitly reference the default User, or if you ever switch back,
    # these unique names prevent migration conflicts.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set',  # Unique related name
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_permissions_set',  # Another unique related name
        related_query_name='customuser_permission',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Keep username required for createsuperuser prompt, but email is primary login

    objects = CustomUserManager()

    def __str__(self):
        """
        Returns a string representation of the user, using email.
        """
        return self.email
