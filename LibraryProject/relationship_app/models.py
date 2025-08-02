# advanced_features_and_security/relationship_app/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class CustomUser(AbstractUser):
    # User roles
    ADMIN = 'ADMIN'
    LIBRARIAN = 'LIBRARIAN'
    MEMBER = 'MEMBER'
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=MEMBER
    )
    # The `AbstractUser` class already provides fields like `username`, `email`, `first_name`, and `last_name`.
    # You can add more fields here if needed.

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def has_permission(self, perm, obj=None):
        """
        Check if the user has a specific permission.
        This is a simple implementation, a real-world app would use Django's
        built-in permission system more extensively.
        """
        if self.is_superuser or self.is_admin:
            return True
        if self.is_librarian and (perm.startswith('relationship_app.can_') or perm.startswith('relationship_app.view_')):
            return True
        return super().has_permission(perm, obj=obj)


# A model for the Author of a Book
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        # A simple constraint to ensure the same author isn't added twice.
        unique_together = ('first_name', 'last_name')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# A model for the Books in the library
class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the book")
    # Link a book to an author. If the author is deleted, their books remain.
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(help_text="A brief summary of the book", null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text="13 Character <a href='https://www.isbn-international.org/content/what-isbn'>ISBN number</a>")
    total_copies = models.PositiveIntegerField(default=1, help_text="Total number of copies available in the library")
    available_copies = models.PositiveIntegerField(default=1, help_text="Number of copies currently available for loan")

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])

# A model to track book loans.
class Loan(models.Model):
    # When a user is deleted, their loans are also deleted.
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # When a book is deleted, its loans are also deleted.
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        # A loan is overdue if there is no return date and the due date has passed.
        from django.utils import timezone
        return self.return_date is None and self.due_date < timezone.now().date()

    def clean(self):
        super().clean()
        if self.due_date < self.loan_date:
            raise ValidationError({'due_date': _("Due date cannot be before the loan date.")})

    def __str__(self):
        return f"{self.user.username} loaned {self.book.title}"

