Django Models Project
This directory serves as the root for the Django project. It contains the main manage.py script for interacting with the project, the primary library_project configuration package, and the relationship_app which defines the application's models and query examples.

Structure Overview
django_models/
├── manage.py               # Django's command-line utility
├── library_project/        # Core project configuration (settings, URLs, WSGI/ASGI)
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── relationship_app/       # Custom Django application
    ├── models.py
    ├── query_samples.py
    └── ...

Getting Started
To set up and run this Django project, please refer to the main README.md in the repository root (../README.md).

Management Commands
All Django management commands should be run from this directory (where manage.py resides).

Example:

python manage.py runserver
python manage.py makemigrations relationship_app
python manage.py migrate
