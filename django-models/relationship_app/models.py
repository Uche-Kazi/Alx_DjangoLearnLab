from django.db import models

# 1. Author Model
# This model represents an author.
# It will be the "one" side in a ForeignKey relationship with Book.
class Author(models.Model):
    name = models.CharField(max_length=100) # The author's name

    def __str__(self):
        return self.name

# 2. Book Model
# This model represents a book.
# It has a ForeignKey relationship with Author (one author can write many books).
# It will have a ManyToMany relationship with Library (one book can be in many libraries,
# and one library can have many books).
class Book(models.Model):
    title = models.CharField(max_length=200) # The title of the book
    # ForeignKey: Links a Book to an Author.
    # on_delete=models.CASCADE means if an Author is deleted, all their books are also deleted.
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 3. Library Model
# This model represents a library.
# It has a ManyToMany relationship with Book (a library can have many books,
# and a book can be in many libraries).
# It will be the "one" side in a OneToOneField relationship with Librarian.
class Library(models.Model):
    name = models.CharField(max_length=100) # The name of the library
    # ManyToManyField: Links a Library to many Books.
    # This creates an intermediary table to manage the relationship.
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

# 4. Librarian Model
# This model represents a librarian.
# It has a OneToOneField relationship with Library (each librarian is associated
# with exactly one library, and each library has one librarian).
# on_delete=models.CASCADE means if a Library is deleted, its Librarian is also deleted.
class Librarian(models.Model):
    name = models.CharField(max_length=100) # The librarian's name
    # OneToOneField: Links a Librarian to a Library.
    # This ensures a 1-to-1 relationship.
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name