import os
import sys # Import the sys module
# Add the project root directory to the Python path
# This allows Django to find the 'LibraryProject' settings module.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Add this line
import django

# Set up Django environment
# This block is crucial for running Django ORM operations outside of manage.py commands.
# It tells the script where your Django project's settings are located.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

# Import the models from your relationship_app
from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    print("--- Running Sample Queries for Model Relationships ---")

    # 1. Create Sample Data
    # This ensures we have data to query.
    print("\n--- Creating Sample Data ---")

    # Authors
    author1, created = Author.objects.get_or_create(name="Jane Austen")
    if created: print(f"Created Author: {author1.name}")
    author2, created = Author.objects.get_or_create(name="George Orwell")
    if created: print(f"Created Author: {author2.name}")
    author3, created = Author.objects.get_or_create(name="J.K. Rowling")
    if created: print(f"Created Author: {author3.name}")

    # Books
    book1, created = Book.objects.get_or_create(title="Pride and Prejudice", author=author1)
    if created: print(f"Created Book: {book1.title} by {book1.author.name}")
    book2, created = Book.objects.get_or_create(title="1984", author=author2)
    if created: print(f"Created Book: {book2.title} by {book2.author.name}")
    book3, created = Book.objects.get_or_create(title="Animal Farm", author=author2)
    if created: print(f"Created Book: {book3.title} by {book3.author.name}")
    book4, created = Book.objects.get_or_create(title="Harry Potter and the Sorcerer's Stone", author=author3)
    if created: print(f"Created Book: {book4.title} by {book4.author.name}")

    # Libraries
    library1, created = Library.objects.get_or_create(name="Central City Library")
    if created: print(f"Created Library: {library1.name}")
    library2, created = Library.objects.get_or_create(name="University Library")
    if created: print(f"Created Library: {library2.name}")

    # Add books to libraries (ManyToMany relationship)
    if created or not library1.books.exists(): # Only add if library is new or has no books
        library1.books.add(book1, book2, book4)
        print(f"Added books to {library1.name}")
    if created or not library2.books.exists():
        library2.books.add(book2, book3)
        print(f"Added books to {library2.name}")

    # Librarians (OneToOne relationship)
    librarian1, created = Librarian.objects.get_or_create(name="Alice Smith", library=library1)
    if created: print(f"Created Librarian: {librarian1.name} for {librarian1.library.name}")
    librarian2, created = Librarian.objects.get_or_create(name="Bob Johnson", library=library2)
    if created: print(f"Created Librarian: {librarian2.name} for {librarian2.library.name}")

    print("\n--- Performing Queries ---")

    # Query 1: Query all books by a specific author (ForeignKey)
    print("\nQuery 1: All books by George Orwell")
    george_orwell = Author.objects.get(name="George Orwell")
    orwell_books = Book.objects.filter(author=george_orwell)
    for book in orwell_books:
        print(f"- {book.title}")

    # Query 2: List all books in a library (ManyToMany)
    print("\nQuery 2: All books in Central City Library")
    central_library = Library.objects.get(name="Central City Library")
    central_library_books = central_library.books.all()
    for book in central_library_books:
        print(f"- {book.title}")

    # Query 3: Retrieve the librarian for a library (OneToOne)
    print("\nQuery 3: Librarian for University Library")
    university_library = Library.objects.get(name="University Library")
    # Access the related Librarian object directly via the reverse relationship
    university_librarian = university_library.librarian # Note: Django automatically creates this reverse accessor
    print(f"- The librarian for {university_library.name} is {university_librarian.name}")

    print("\n--- Queries Complete ---")

if __name__ == "__main__":
    run_queries()
