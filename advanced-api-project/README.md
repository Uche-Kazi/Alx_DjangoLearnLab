Advanced API Project: Book Management API
This project demonstrates building a RESTful API for managing Authors and Books using Django and Django REST Framework.

Features Implemented in this Task: Custom Views and Generic Views
This section details the API endpoints for the Book model, implemented using Django REST Framework's Generic Views and Mixins, along with permission handling.

Views (api/views.py)
We utilize DRF's generics.ListCreateAPIView and generics.RetrieveUpdateDestroyAPIView for efficient CRUD operations on the Book model.

BookListCreateView:

Purpose: Handles listing all Book instances and creating new ones.

HTTP Methods Handled:

GET /api/books/: Retrieves a list of all books.

POST /api/books/: Creates a new book.

Permissions: permissions.IsAuthenticatedOrReadOnly

Unauthenticated users: Can perform GET requests (read-only).

Authenticated users: Can perform GET and POST requests.

Validation: Data validation (including custom publication_year validation) is handled automatically by the BookSerializer.

BookDetailView:

Purpose: Handles retrieving, updating, and deleting a single Book instance by its ID.

HTTP Methods Handled:

GET /api/books/<int:pk>/: Retrieves a single book.

PUT /api/books/<int:pk>/: Fully updates an existing book.

PATCH /api/books/<int:pk>/: Partially updates an existing book.

DELETE /api/books/<int:pk>/: Deletes an existing book.

Permissions: permissions.IsAuthenticatedOrReadOnly

Unauthenticated users: Can perform GET requests (read-only).

Authenticated users: Can perform GET, PUT, PATCH, and DELETE requests.

Validation: Data validation is handled automatically by the BookSerializer.

URL Patterns (api/urls.py & advanced_api_project/urls.py)
The following endpoints are configured:

/api/books/ (Maps to BookListCreateView)

GET: List all books.

POST: Create a new book.

/api/books/<int:pk>/ (Maps to BookDetailView)

GET: Retrieve a book by ID.

PUT: Update a book by ID.

PATCH: Partially update a book by ID.

DELETE: Delete a book by ID.

Permissions (Global and View-Specific)
Global Configuration (settings.py):
REST_FRAMEWORK is configured to use TokenAuthentication by default for authentication and IsAuthenticatedOrReadOnly as the default permission class.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}

View-Specific Permissions:
The permission_classes = [permissions.IsAuthenticatedOrReadOnly] is explicitly applied to BookListCreateView and BookDetailView, overriding any global default if they were different. This ensures:

Anyone can read (view) the book data.

Only authenticated users can modify (create, update, delete) book data.

How to Test
To test these endpoints:

Ensure server is running: python manage.py runserver

Obtain an Authentication Token:
If you are testuser (password testpass123), use:
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass123"}' http://127.0.0.1:8000/api-token-auth/
(Copy the token from the response).

Use curl (or Postman/Insomnia) with the following headers (for authenticated requests):
Content-Type: application/json
Authorization: Token YOUR_AUTH_TOKEN

Example authenticated POST:
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token YOUR_AUTH_TOKEN" -d '{"title": "New Book", "publication_year": 2024, "author": 1}' http://127.0.0.1:8000/api/books/