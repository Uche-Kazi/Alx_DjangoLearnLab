# ~/Alx_DjangoLearnLab/django_blog/django_blog/settings.py

import os
from pathlib import Path
from django.contrib.messages import constants as messages # Required for MESSAGE_TAGS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m#x7^13$e)u%k5o(u#c7!t#9v1!+k71-z%t!s-!2x2z&t%j!f' # Ensure your actual secret key is here

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Add your domain names or IP addresses here for production.
# For local development, '127.0.0.1' and 'localhost' are usually sufficient.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My apps
    'accounts.apps.AccountsConfig', # Your custom user app is here
    'blog.apps.BlogConfig',         # Your blog app is here
    # 'users.apps.UsersConfig',     # <-- REMOVED: This app does not exist
    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap4',            # Using Bootstrap 4/5 template pack for Crispy Forms
]

# MIDDLEWARE configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_blog.urls'

# TEMPLATES configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Use Path object for consistency
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_blog.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Use Path object
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Use Path object

# Media files settings (for user-uploaded content like profile pictures)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model configuration
# AUTH_USER_MODEL = 'accounts.CustomUser' # Correctly points to your CustomUser in the 'accounts' app

# Authentication Redirect URLs
# Redirect to the home page of the blog app after successful login
LOGIN_REDIRECT_URL = 'blog:home'
# URL for the login page, used by @login_required decorator
LOGIN_URL = 'login'
# Redirect to the logged out page after successful logout (assuming 'logged_out' URL is defined)
LOGOUT_REDIRECT_URL = 'logged_out'

# CRISPY FORMS SETTINGS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4' # Use bootstrap4 as your templates are Bootstrap based

# Message Tags for Bootstrap styling
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
