"""
ASGI config for library_project project.
"""

import os

from django.core.asgi import get_asgi_application

# CRITICAL: Settings module is now library_project.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')

application = get_asgi_application()
