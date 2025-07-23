Migrations for Relationship App
This directory contains database migrations for the relationship_app. Migrations are Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. This folder is located within the relationship_app, which is now a sibling to the inner LibraryProject package.

Contents
__init__.py: Marks this directory as a Python package.

0001_initial.py (and subsequent files): These are auto-generated Python files that represent changes to your database schema. Do not edit these files manually unless you fully understand Django's migration system.

How Migrations Work
When you run python manage.py makemigrations relationship_app, Django inspects your models.py file, compares it to the current state of your migrations, and generates new migration files if changes are detected.

When you run python manage.py migrate, Django applies these migration files to your database, updating the schema.

Structure Context
This folder is part of the following path within the repository:
Alx_DjangoLearnLab/django-models/LibraryProject/relationship_app/migrations/