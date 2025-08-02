# bookshelf/models.py
from django.db import models
from django.utils import timezone

# This is our first model. It defines the structure of the data
# for our books. Each class attribute represents a database field.
# Django automatically creates a primary key for each model.
class Book(models.Model):
    """
    A model to represent a single book in the library.
    """
    # CharField is used for short strings.
    # The max_length parameter is required.
    title = models.CharField(max_length=200)

    # We use CharField for the author's name as well.
    author = models.CharField(max_length=100)

    # DateField is used to store dates.
    # The default value is set to the current date and time.
    publication_date = models.DateField(default=timezone.now)

    # This is a special method in Django models that provides a
    # human-readable representation of the object.
    def __str__(self):
        return f"{self.title} by {self.author}"
