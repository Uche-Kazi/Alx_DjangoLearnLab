# LibraryProject/relationship_app/models.py

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.conf import settings # Import settings to reference AUTH_USER_MODEL

# --- Custom User Model ---
class CustomUser(AbstractUser):
    """
    Extends the built-in AbstractUser model with a 'role' field
    and other profile information.
    """
    # Define role choices as constants directly on CustomUser
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)

    # You can move other fields from your old UserProfile here if they were essential
    # For example:
    # date_of_birth = models.DateField(null=True, blank=True)
    # address = models.CharField(max_length=300, blank=True, null=True)
    # phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

# --- Core Library Models ---

class Author(models.Model):
    """
    Represents an author of a book.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    """
    Represents a book in the library.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='books')
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    available_copies = models.IntegerField(default=1)
    total_copies = models.IntegerField(default=1)

    @property
    def is_available(self):
        return self.available_copies > 0

    def __str__(self):
        return f"{self.title} by {self.author.first_name} {self.author.last_name}" if self.author else self.title

class Library(models.Model):
    """
    Represents a physical library location.
    """
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Libraries"

    def __str__(self):
        return self.name

class Librarian(models.Model):
    """
    Represents a librarian associated with a library.
    This model now links to our CustomUser.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True, related_name='librarians')
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    hire_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Librarian: {self.user.username} ({self.employee_id})"

# UserProfile model is removed
# class UserProfile(models.Model):
#     ...

class Loan(models.Model):
    """
    Represents a loan of a book to a user (member).
    This model now links to our CustomUser.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        status = " (Returned)" if self.return_date else " (Active)"
        return f"{self.book.title} loaned to {self.user.username}{status}"

    class Meta:
        unique_together = ('book', 'user', 'return_date')
        verbose_name = "Book Loan"
        verbose_name_plural = "Book Loans"

# post_save signal for UserProfile is removed
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     ...
