# LibraryProject/relationship_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        ordering = ['last_name', 'first_name'] # Order authors by last name, then first name

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
    available_copies = models.IntegerField(default=1) # Track available copies
    total_copies = models.IntegerField(default=1) # Track total copies

    @property
    def is_available(self):
        """Checks if there are any available copies of the book."""
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
        verbose_name_plural = "Libraries" # Corrected plural form for admin interface

    def __str__(self):
        return self.name

class Librarian(models.Model):
    """
    Represents a librarian associated with a library.
    This model extends the built-in User model using a OneToOneField.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True, related_name='librarians')
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    hire_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Librarian: {self.user.username} ({self.employee_id})"

# --- User Profile and Book Assignment Models ---

class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile information.
    Includes a 'role' field to define user types.
    """
    # Define role choices as constants
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'

    USER_ROLES = (
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=20, choices=USER_ROLES, default=MEMBER) # Use constant as default
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username} ({self.role})"

class Loan(models.Model):
    """
    Represents a loan of a book to a user (member).
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # Ensure this is 'user' and not 'member' or anything else
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        status = " (Returned)" if self.return_date else " (Active)"
        return f"{self.book.title} loaned to {self.user.username}{status}"

    class Meta:
        # Ensure a book can only be actively loaned to a user once at a time
        # If you changed 'member' to 'user', this unique_together might need a migration too.
        unique_together = ('book', 'user', 'return_date')
        verbose_name = "Book Loan"
        verbose_name_plural = "Book Loans"

# --- Signals for UserProfile Creation ---

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates or updates a UserProfile when a User is created or updated.
    Ensures that every User has a corresponding UserProfile.
    """
    if created:
        UserProfile.objects.create(user=instance, role=UserProfile.MEMBER)
    else:
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance, role=UserProfile.MEMBER)
