import os
import sys
import django

# Adjust the Python path to include the project root (django-models).
# This is crucial for running Django ORM operations from a script
# nested inside an app, allowing it to find the 'LibraryProject.settings'.
# __file__ is django-models/relationship_app/query_samples.py
# os.path.abspath(__file__) -> .../Alx_DjangoLearnLab/django-models/relationship_app/query_samples.py
# os.path.dirname(...) -> .../Alx_DjangoLearnLab/django-models/relationship_app/
# os.path.dirname(os.path.dirname(...)) -> .../Alx_DjangoLearnLab/django-models/
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root_path not in sys.path:
    sys.path.append(project_root_path)

# Set up Django environment
# The settings module is LibraryProject.settings, as LibraryProject is the inner package.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# Import the models from your relationship_app
from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author (ForeignKey)
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
        return Book.objects.none() # Return an empty queryset if author not found

# List all books in a specific library (ManyToMany)
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
        return Book.objects.none() # Return an empty queryset if library not found

# Retrieve the librarian for a specific library (OneToOne)
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
        # Access the related Librarian object directly via the reverse relationship
        return library.librarian
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None # Return None if a library exists but has no assigned librarian

# --- Optional: For local testing only ---
# You can uncomment and run this block locally to test the functions.
# Remember to run `python manage.py shell` and create some data first,
# or add temporary data creation here for quick testing.
"""
if __name__ == "__main__":
    print("--- Local Testing of Query Functions ---")

    # IMPORTANT: For this local test block to work, you need data in your DB.
    # You can either run this from `python manage.py shell` after creating data,
    # or temporarily add data creation here (but remove it before pushing to checker).

    # Example of temporary data creation for local testing (REMOVE BEFORE PUSHING)
    # try:
    #     author_jk, _ = Author.objects.get_or_create(name="J.K. Rowling")
    #     author_geo, _ = Author.objects.get_or_create(name="George Orwell")
    #     book_hp, _ = Book.objects.get_or_create(title="Harry Potter", author=author_jk)
    #     book_1984, _ = Book.objects.get_or_create(title="1984", author=author_geo)
    #     lib_central, _ = Library.objects.get_or_create(name="Central Library")
    #     lib_central.books.add(book_hp, book_1984)
    #     librarian_alice, _ = Librarian.objects.get_or_create(name="Alice", library=lib_central)
    # except Exception as e:
    #     print(f"Error creating test data: {e}. Ensure migrations are applied.")


    # Test Query 1
    print("\nBooks by J.K. Rowling:")
    books = books_by_author("J.K. Rowling")
    for book in books:
        print(f"- {book.title}")

    # Test Query 2
    print("\nBooks in Central Library:")
    books = books_in_library("Central Library")
    for book in books:
        print(f"- {book.title}")

    # Test Query 3
    print("\nLibrarian for Central Library:")
    librarian = librarian_for_library("Central Library")
    if librarian:
        print(f"- {librarian.name}")
    else:
        print("- No librarian found.")
"""
