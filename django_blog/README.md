User Authentication System Documentation
This document outlines the implementation of a custom user authentication system for the Django blog project, covering model definitions, forms, views, URL configurations, template integration, and necessary third-party library installations.

1. Overview of the Authentication System
The authentication system is built upon Django's extendable AbstractUser model, allowing for future customization beyond the default user fields. It includes:

A custom user model (CustomUser).

Custom registration and change forms (UserRegisterForm, CustomUserChangeForm).

Function-based views for user registration and logout, and a class-based view for the profile page.

Integration with Django's built-in LoginView and LogoutView.

Dedicated URL patterns for all authentication-related actions.

Styled templates using django-crispy-forms and crispy-tailwind.

2. Detailed File Changes and Explanations
django_blog/settings.py
This file was updated to:

INSTALLED_APPS:

Include 'accounts.apps.AccountsConfig' to register the accounts app.

Include 'blog.apps.BlogConfig' to register the blog app.

Add 'crispy_forms' and 'crispy_tailwind' to enable the django-crispy-forms library for enhanced form rendering.

AUTH_USER_MODEL = 'accounts.CustomUser': This crucial setting tells Django to use our custom CustomUser model from the accounts app instead of Django's default User model. This must be set before any migrations are run for django.contrib.auth.

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind": Defines which template packs Crispy Forms is allowed to use.

CRISPY_TEMPLATE_PACK = "tailwind": Sets "tailwind" as the default template pack for django-crispy-forms, ensuring forms are rendered with Tailwind CSS classes.

LOGIN_REDIRECT_URL = 'profile': Specifies the URL name to redirect users to after a successful login.

LOGOUT_REDIRECT_URL = 'logged_out': Specifies the URL name to redirect users to after a successful logout.

LOGIN_URL = 'login': Defines the URL name for the login page, used by decorators like @login_required and by the authentication system itself.

django_blog/urls.py
The main project urls.py was updated to:

path('accounts/', include('accounts.urls')): Include all URL patterns defined in accounts/urls.py under the /accounts/ prefix.

path('', include('blog.urls')): Include URLs from the blog app, making its root URL ('') the homepage.

path('logged_out/', account_views.logged_out, name='logged_out'): Explicitly define a project-level URL for the logged_out page.

accounts/models.py
This file defines the custom user model:

CustomUser(AbstractUser): Inherits from Django's AbstractUser, providing all default authentication fields (username, password, email, first name, last name, staff status, superuser status, etc.). Additional custom fields can be added here if needed in the future.

__str__ method returns the username for easy identification.

accounts/forms.py
This file contains custom forms for user management:

UserRegisterForm(UserCreationForm):

Extends UserCreationForm to handle registration logic.

Adds an email field and makes it required, overriding the default UserCreationForm which doesn't enforce email.

Includes custom clean_email validation to ensure unique email addresses.

model = User (Note: While AUTH_USER_MODEL is CustomUser, UserCreationForm typically works with django.contrib.auth.models.User by default, but when AUTH_USER_MODEL is set, it correctly uses CustomUser. The model = User in Meta here refers to the underlying behavior of UserCreationForm before AUTH_USER_MODEL fully overrides, but for a custom model, it should explicitly be model = CustomUser. This has been updated to model = CustomUser in the final code to be precise.)

CustomUserChangeForm(UserChangeForm):

Extends UserChangeForm for editing existing users in the Django admin.

model = CustomUser: Explicitly associates with the CustomUser model.

fields: Defines which fields are editable in the admin change form.

accounts/views.py
This file contains the view logic for user authentication:

signup(request) (Function-based view):

Handles GET (display form) and POST (process form) requests for user registration.

Uses UserRegisterForm.

Upon successful registration, saves the user, displays a success message using Django's messages framework, and redirects to the 'login' page.

profile(request) (Function-based view with @login_required):

Requires the user to be logged in to access.

Renders the accounts/profile.html template.

logged_out(request) (Function-based view):

Renders a simple page indicating the user has been logged out.

Displays an informational message using Django's messages framework.

Django's Built-in Views Integration (handled in accounts/urls.py):

django.contrib.auth.views.LoginView: Used for the login page, rendering accounts/login.html.

django.contrib.auth.views.LogoutView: Used for logout, redirecting to the URL named 'logged_out'.

accounts/urls.py
This file defines the URL patterns for the accounts app:

path('signup/', views.signup, name='signup'): Maps /accounts/signup/ to the signup view.

path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'): Maps /accounts/login/ to Django's built-in LoginView.

path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name='logout'): Maps /accounts/logout/ to Django's built-in LogoutView.

path('profile/', views.profile, name='profile'): Maps /accounts/profile/ to the profile view.

accounts/admin.py
This file customizes the Django administration interface for the CustomUser model:

CustomUserAdmin(UserAdmin): Creates a custom admin class for CustomUser by extending Django's default UserAdmin.

add_form = UserRegisterForm: Specifies the form to use when adding a new user in the admin.

form = CustomUserChangeForm: Specifies the form to use when changing an existing user in the admin.

model = CustomUser: Links the admin class to our custom user model.

list_display = ['email', 'username']: Configures which fields are shown in the list view of users in the admin.

admin.site.register(CustomUser, CustomUserAdmin): Registers the CustomUser model with our custom admin class.

Templates
All templates were created or updated to:

Extend blog/base.html: {% extends "blog/base.html" %} ensures a consistent look and feel across all pages.

Use {% load crispy_forms_tags %}: For forms, this tag library enables the {{ form|crispy }} filter for Tailwind-styled rendering.

Implement {% block title %} and {% block content %}: These blocks define specific content areas within the base template.

blog/templates/blog/base.html: Contains the basic HTML structure, including the navigation bar with conditional links for authenticated/unauthenticated users (Home, Profile, Logout/Login, Register).

accounts/templates/accounts/signup.html: Provides the HTML structure for the user registration form, utilizing {{ form|crispy }}.

accounts/templates/accounts/login.html: Provides the HTML structure for the user login form.

accounts/templates/accounts/profile.html: A basic page displaying user information for logged-in users.

accounts/templates/accounts/logged_out.html: A simple page displayed after a user logs out, with options to log in again or return home.

3. Migration Process
The following steps were crucial for applying database changes related to the custom user model:

Deletion of db.sqlite3 and app-specific migration files: This ensured a clean slate, removing any potential inconsistencies from previous attempts.

python manage.py makemigrations: Created new migration files for all apps, especially accounts/0001_initial.py for CustomUser.

python manage.py migrate: Applied all pending migrations to the database, creating the accounts_customuser table.

python manage.py createsuperuser: Created an administrative user in the newly created accounts_customuser table, allowing access to the Django admin panel.

4. Installation of Third-Party Libraries
pip install django-crispy-forms: Installed the core library for form rendering.

pip install crispy-tailwind: Installed the specific Tailwind CSS template pack for django-crispy-forms.

5. Testing Strategy
The authentication system was tested by:

Accessing the homepage (/) to confirm basic site functionality.

Logging into the Django admin (/admin/) with a newly created superuser to verify CustomUser integration.

Navigating to the registration page (/accounts/signup/) to confirm form rendering and submission.

Successfully registering a new test user account.

Verifying the newly registered user in the Django admin.

Testing login with the newly registered user.

Testing logout functionality.

This documentation provides a complete overview of the implemented user authentication system. You can now proceed with your git commit, git push, and run the checker.