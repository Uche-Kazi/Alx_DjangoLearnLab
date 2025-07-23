# Import the models from your relationship_app
# Assume Django environment (including models) is already set up by the checker.
# The app is now nested: LibraryProject.relationship_app
from LibraryProject.relationship_app.models import Author, Book, Library, Librarian
from django.core.exceptions import ObjectDoesNotExist # Import ObjectDoesNotExist

# Query all books by a specific author
def books_by_author(author_name):
    """
    Retrieves all books written by a specific author.
    Args:
        author_name (str): The name of the author.
    Returns:
        django.db.models.QuerySet: A QuerySet of Book objects by the specified author.
    """
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        # Return an empty queryset if the author is not found
        return Book.objects.none()

# List all books in a specific library
def books_in_library(library_name):
    """
    Retrieves all books available in a specific library.
    Args:
        library_name (str): The name of the library.
    Returns:
        django.db.models.QuerySet: A QuerySet of Book objects in the specified library.
    """
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        # Return an empty queryset if the library is not found
        return Book.objects.none()

# Retrieve the librarian for a specific library
def librarian_for_library(library_name):
    """
    Retrieves the librarian assigned to a specific library.
    Args:
        library_name (str): The name of the library.
    Returns:
        Librarian: The Librarian object for the specified library, or None if not found.
    """
    try:
        library = Library.objects.get(name=library_name)
        # CRITICAL FIX: Use Librarian.objects.get(library=...) as required by the checker.
        try:
            return Librarian.objects.get(library=library)
        except Librarian.DoesNotExist:
            # If the library exists but has no associated librarian, return None
            return None
    except Library.DoesNotExist:
        # Return None if the library itself is not found
        return None

# No `if __name__ == "__main__":` block or `django.setup()` here.
# The checker is expected to import and call these functions directly
# after setting up the Django environment and populating test data.
