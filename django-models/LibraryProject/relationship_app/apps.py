# LibraryProject/relationship_app/apps.py

from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LibraryProject.relationship_app'

    def ready(self):
        # The 'pass' statement should be directly under the 'def ready(self):'
        pass 
