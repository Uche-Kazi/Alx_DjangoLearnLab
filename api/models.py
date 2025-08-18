# ~/Alx_DjangoLearnLab/api/models.py

from django.db import models

class Author(models.Model):
    """
    Model representing an Author.
    Fields:
    - name: CharField for the author's name.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        String representation of the Author model.
        """
        return self.name

class Book(models.Model):
    """
    Model representing a Book.
    Fields:
    - title: CharField for the book's title.
    - publication_year: IntegerField for the year the book was published.
    - author: ForeignKey linking to the Author model (one-to-many relationship).
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        """
        String representation of the Book model.
        """
        return f"{self.title} by {self.author.name}"

