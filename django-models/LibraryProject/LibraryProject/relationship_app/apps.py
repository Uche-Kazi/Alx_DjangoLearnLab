from django.apps import AppConfig


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LibraryProject.LibraryProject.relationship_app' # CRITICAL: App name is now deeply nested
