# ~/Alx_DjangoLearnLab/api_project/api/models.py

from django.db import models

class Book(models.Model):
    """
    A simple model representing a book for API demonstration.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        """
        String representation for the Book model, useful in Django Admin.
        """
        return f"{self.title} by {self.author}"

