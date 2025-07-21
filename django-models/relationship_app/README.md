Relationship App
This Django application (relationship_app) is designed to demonstrate various types of model relationships (One-to-Many, Many-to-Many, One-to-One) within a library management context. It defines the core data structures for authors, books, libraries, and librarians.

Models Defined
Author: Represents authors of books.

Book: Represents books, with a ForeignKey relationship to Author.

Library: Represents libraries, with a ManyToMany relationship to Book.

Librarian: Represents librarians, with a OneToOne relationship to Library.

Query Samples
The query_samples.py file provides examples of how to interact with these models using Django's ORM (Object-Relational Mapper) to retrieve data based on the defined relationships.

To test these queries, navigate to the django-models/ directory in your terminal and run:

python manage.py shell

Then, import functions from query_samples.py and experiment.

Migrations
Database schema changes for these models are managed in the migrations/ subdirectory.