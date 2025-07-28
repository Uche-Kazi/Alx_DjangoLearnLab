# LibraryProject/relationship_app/apps.py

from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LibraryProject.relationship_app' # Ensure this matches your INSTALLED_APPS entry

    def ready(self):
        """
        Import signals when the app is ready.
        """
        import LibraryProject.relationship_app.signals # Import your signals.py
