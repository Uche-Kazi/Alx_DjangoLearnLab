Django Models Project Root
This directory serves as the primary root for the Django project. It contains the main manage.py script for interacting with the project and an intermediate LibraryProject folder that holds the core project configuration and applications.

Structure Overview
django-models/
├── manage.py               # Django's command-line utility
├── LibraryProject/         # Intermediate folder (holds inner project and apps)
│   ├── LibraryProject/     # Core project configuration (settings, URLs, WSGI/ASGI)
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   └── relationship_app/   # Custom Django application
│       ├── models.py
│       ├── query_samples.py
│       └── ...
├── README.md               # This file
└── ... (other files like db.sqlite3, .gitignore, etc.)

Getting Started
To set up and run this Django project, ensure you are in this django-models/ directory and refer to the main README.md in the repository root (../README.md).

Management Commands
All Django management commands should be run from this directory (where manage.py resides).

Example:

python manage.py runserver
python manage.py makemigrations relationship_app
python manage.py migrate
