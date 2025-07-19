"""
WSGI config for library_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

# CRITICAL: Settings module is now library_project.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')

application = get_wsgi_application()
