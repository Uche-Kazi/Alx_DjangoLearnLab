Library Management System
This is a Django-based web application for managing a library's book collection and user permissions. This project was developed as part of the ALX Django Learn Lab, with a strong focus on implementing security best practices.

Features
User Authentication: Users can register, log in, and log out using a custom user model that authenticates via email.

Book Management:

Books can be created, viewed, edited, and deleted.

Book data includes title, author, published date, and ISBN.

Permissions and Roles:

The system uses custom permissions (can_create, can_edit, can_delete) to control access to different features.

Users are assigned to groups (Admins, Editors, Viewers) that grant specific permissions.

Author Management: Authors can be created and managed.

Security Best Practices Implemented
This application incorporates several security measures to protect against common web vulnerabilities:

Debug Mode Off: DEBUG is set to False in settings.py to prevent sensitive information disclosure in production.

Host Header Protection: ALLOWED_HOSTS is configured to prevent HTTP Host header attacks.

XSS Protection:

SECURE_BROWSER_XSS_FILTER is enabled to activate browser-side XSS filters.

SECURE_CONTENT_TYPE_NOSNIFF is enabled to prevent MIME-sniffing attacks.

All user inputs are validated and sanitized using Django Forms and the ORM, preventing SQL Injection and input-based XSS.

CSRF Protection:

CSRF_COOKIE_SECURE is set to True to ensure CSRF tokens are transmitted only over HTTPS.

All forms include {% csrf_token %} to protect against Cross-Site Request Forgery attacks.

Clickjacking Protection: X_FRAME_OPTIONS is set to DENY to prevent the site from being embedded in iframes on other domains.

Session Security: SESSION_COOKIE_SECURE is set to True to ensure session cookies are transmitted only over HTTPS.

Content Security Policy (CSP): Implemented using django-csp middleware, defining strict rules ('self' for most sources, 'none' for objects/frames) to mitigate XSS by controlling resource loading.

Directory Structure
The project has a nested structure as required by the ALX checker:

advanced_features_and_security/

LibraryProject/

bookshelf/ (The main application for managing books)

accounts/ (User authentication and profile management)

LibraryProject/ (Project-level settings, URLs, etc.)

manage.py

README.md (This file)

How to Run
Clone the Repository: Clone this project to your local machine.

Create and Activate a Virtual Environment:

python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

Install Dependencies:

pip install Django django-csp

Navigate to the LibraryProject directory:

cd advanced_features_and_security/LibraryProject

Run Migrations:

python manage.py makemigrations
python manage.py migrate

Create a Superuser: This user will be able to access the admin site to set up groups and permissions.

python manage.py createsuperuser

Run the Development Server:

python manage.py runserver

Your application will now be running at http://127.0.0.1:8000/.

Testing Security Measures
After running the server, you can manually test the implemented security:

CSRF: Attempt to submit a form after manually removing the {% csrf_token %} tag from the template. You should get a 403 Forbidden error.

XSS: Try entering <script>alert('XSS')</script> into a book title or author name. The script should not execute.

Clickjacking: Try embedding your site in an iframe on a different domain. It should be blocked by the browser.

CSP: Use your browser's developer tools (Network tab, then inspect headers) to confirm the Content-Security-Policy header is present. Try to load an external script from an untrusted domain (e.g., by temporarily adding <img> tag with src from external domain) and observe if it's blocked in the console.