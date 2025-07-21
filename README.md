Alx_DjangoLearnLab
This repository serves as a learning lab for Django, focusing on fundamental concepts such as project structure, model definitions, and database migrations.

It contains a Django project named django-models which includes a relationship_app designed to demonstrate various Django model relationships (ForeignKey, ManyToMany, OneToOne).

Project Structure
The core Django project resides within the django-models/ directory.

Alx_DjangoLearnLab/
├── django-models/              # Main Django project root
│   ├── manage.py
│   ├── LibraryProject/         # Main project configuration (settings, URLs)
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── relationship_app/       # Django application for models and queries
│   │   ├── models.py
│   │   ├── query_samples.py
│   │   └── ...
│   └── ...
└── venv/                       # Python virtual environment

Setup and Installation
Clone the repository:

git clone https://github.com/Uche-Kazi/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Django:

pip install Django==5.2.4

Navigate into the Django project directory:

cd django-models

Run database migrations:

python manage.py makemigrations relationship_app
python manage.py migrate

Run the development server (optional):

python manage.py runserver

Usage
Explore the relationship_app/models.py for model definitions and relationship_app/query_samples.py for example database queries. You can test these queries in the Django shell:

python manage.py shell

Then, within the shell:

from relationship_app.query_samples import books_by_author, books_in_library, librarian_for_library

# Example usage:
# books_by_author("J.K. Rowling")
# books_in_library("Central Library")
# librarian_for_library("Community Library")
