# my_library_project/bookshelf/models.py

from django.db import models

class Author(models.Model):
    """
    Model for a book author.
    """
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model for a book. Includes custom permissions.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    
    # Define custom permissions for the Book model
    class Meta:
        permissions = [
            ("can_view", "Can view book details"),
            ("can_create", "Can create a new book"),
            ("can_edit", "Can edit an existing book"),
            ("can_delete", "Can delete a book"),
        ]

    def __str__(self):
        return self.title

class Loan(models.Model):
    """
    Model to track book loans.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} loaned to {self.user.username}"
