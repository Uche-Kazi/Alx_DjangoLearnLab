Advanced API Project: Book Management API
This project demonstrates building a RESTful API for managing Authors and Books using Django and Django REST Framework.

Features Implemented in this Task: Filtering, Searching, and Ordering
This section details the enhanced query capabilities added to the Book API endpoints, allowing consumers to efficiently filter, search, and sort book data.

Views (api/views.py)
The BookListView has been updated to incorporate these functionalities using Django REST Framework's filter backends.

BookListView Enhancements:

Filtering: Implemented using django_filters.rest_framework.DjangoFilterBackend.

Filterable fields: title, author (by ID), publication_year.

Usage Example:

Get books by a specific title: GET /api/books/?title=1984

Get books by a specific author ID: GET /api/books/?author=1

Get books published in a specific year: GET /api/books/?publication_year=1997

Searching: Implemented using rest_framework.filters.SearchFilter.

Searchable fields: title, author__name (searches on the related Author's name).

Usage Example:

Search for "Harry Potter" in titles: GET /api/books/?search=Harry%20Potter

Search for books by author name containing "Stephen": GET /api/books/?search=Stephen

Ordering: Implemented using rest_framework.filters.OrderingFilter.

Orderable fields: title, publication_year.

Usage Example:

Order by title (ascending): GET /api/books/?ordering=title

Order by publication year (descending): GET /api/books/?ordering=-publication_year

Combined Usage: You can combine these parameters.

Example: Get books by Stephen E. Lucas, ordered by publication year descending:
GET /api/books/?author=1&ordering=-publication_year

Global DRF Configuration (advanced_api_project/settings.py)
The django_filters app has been added to INSTALLED_APPS to enable the filtering backend.

INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters', # New addition
    # ...
]

How to Test
To test these enhanced API endpoints:

Ensure server is running: python manage.py runserver

Obtain an Authentication Token: If you are testuser (password testpass123), use:
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass123"}' http://127.0.0.1:8000/api-token-auth/
(Copy the token from the response).

Use curl (or Postman/Insomnia) with the following headers (for authenticated requests):
Content-Type: application/json
Authorization: Token YOUR_AUTH_TOKEN

Then, append the desired query parameters (?title=..., ?search=..., ?ordering=...) to http://127.0.0.1:8000/api/books/.