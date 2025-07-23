"""
ASGI config for LibraryProject project.
"""

import os

from django.core.asgi import get_asgi_application

# CRITICAL: Settings module is now LibraryProject.LibraryProject.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.LibraryProject.settings')

application = get_asgi_application()
