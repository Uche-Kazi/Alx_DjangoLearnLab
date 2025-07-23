"""
WSGI config for LibraryProject project.
"""

import os

from django.core.wsgi import get_wsgi_application

# CRITICAL: Settings module is now LibraryProject.LibraryProject.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.LibraryProject.settings')

application = get_wsgi_application()
