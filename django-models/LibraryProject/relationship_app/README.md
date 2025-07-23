Relationship App
This Django application (relationship_app) is designed to demonstrate various types of model relationships (One-to-Many, Many-to-Many, One-to-One) within a library management context. It defines the core data structures for authors, books, libraries, and librarians. This app is now located as a sibling to the inner LibraryProject package, within the intermediate LibraryProject folder, and ultimately within the django-models project root.

Models Defined
Author: Represents authors of books.

Book: Represents books, with a ForeignKey relationship to Author.

Library: Represents libraries, with a ManyToMany relationship to Book.

Librarian: Represents librarians, with a OneToOne relationship to Library.

Query Samples
The query_samples.py file provides examples of how to interact with these models using Django's ORM (Object-Relational Mapper) to retrieve data based on the defined relationships.

To test these queries, navigate to the django-models/ directory in your terminal and run:

python manage.py shell

Then, within the shell:

from LibraryProject.relationship_app.query_samples import books_by_author, books_in_library, librarian_for_library

# Example usage:
# books_by_author("J.K. Rowling")
# books_in_library("Central Library")
# librarian_for_library("Community Library")

Structure Context
This folder is part of the following path within the repository:
Alx_DjangoLearnLab/django-models/LibraryProject/relationship_app/