# ~/Alx_DjangoLearnLab/my_project/my_app/models.py

from django.db import models

class Book(models.Model):
    """
    Model representing a book with a title, author, and published date.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    def __str__(self):
        """
        String representation for the Book model, useful in Django Admin.
        """
        return f"{self.title} by {self.author}"

