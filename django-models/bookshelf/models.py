from django.db import models

    # Define the Book model with specified fields
class Book(models.Model):
        # CharField for the title with a maximum length of 200 characters.
        title = models.CharField(max_length=200)
        # CharField for the author with a maximum length of 100 characters.
        author = models.CharField(max_length=100)
        # IntegerField for the publication year.
        publication_year = models.IntegerField()

        # __str__ method provides a human-readable representation of the Book object.
        # This is very useful in the Django admin and shell.
        def __str__(self):
            return f"{self.title} by {self.author} ({self.publication_year})"
