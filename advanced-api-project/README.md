Advanced API Project: Book Management API
(... existing content ...)

Unit Testing
Comprehensive unit tests have been developed to ensure the integrity, functionality, and security of the API endpoints. These tests cover CRUD operations, filtering, searching, ordering, and authentication/permission enforcement.

Test File Location
All unit tests are located in:
api/test_views.py

Testing Strategy
The tests leverage Django REST Framework's APITestCase to simulate HTTP requests to the API endpoints. Each test case focuses on a specific scenario:

Authentication & Permissions:

Tests verify that unauthenticated users can only perform read operations (GET) and are denied write operations (POST, PUT, DELETE) with a 401 Unauthorized status.

Tests confirm that authenticated users can successfully perform all CRUD operations.

CRUD Operations:

POST requests are tested to ensure new books are created correctly and return 201 Created.

GET requests for lists and details are tested to ensure data integrity and 200 OK status.

PUT/PATCH requests are tested for successful updates (200 OK) and data verification.

DELETE requests are tested for successful removal (204 No Content).

Filtering, Searching, and Ordering:

Tests confirm that API responses are correctly filtered by title, author ID, and publication_year.

Tests verify that search queries on title and author__name return relevant results.

Tests confirm that results are correctly ordered by title (ascending) and publication_year (descending).

How to Run Tests
To execute the full test suite for the api app:

Navigate to your project's root directory (~/Alx_DjangoLearnLab/advanced-api-project/):

cd ~/Alx_DjangoLearnLab/advanced-api-project/

Activate your virtual environment (if not already active):

source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

Run the test command:

python manage.py test api

Interpreting Test Results
OK: All tests passed successfully.

FAILED (failures=X): Indicates that X number of test cases failed. Details of each failure (e.g., AssertionError with expected vs. actual values) will be displayed in the output.

ERROR (errors=X): Indicates that X number of tests encountered unexpected errors (e.g., exceptions during test setup or execution).

A successful test run will show OK at the end, confirming the stability and correctness of your API.