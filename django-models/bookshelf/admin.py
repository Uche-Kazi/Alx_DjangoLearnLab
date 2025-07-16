from django.contrib import admin
from .models import Book # Import your Book model

    # Define the custom admin class for the Book model
class BookAdmin(admin.ModelAdmin):
        # Customize the fields displayed in the list view of the admin interface.
        # This makes it easy to see key information about each book at a glance.
    list_display = ('title', 'author', 'publication_year')

        # Add filters to the right sidebar of the admin list view.
        # Users can filter books by publication year, which is useful for browsing.
    list_filter = ('publication_year',)

        # Enable search functionality in the admin list view.
        # Users can search by title or author, making it easy to find specific books.
    search_fields = ('title', 'author')

        # Optional: Add a date hierarchy for publication_year if it were a DateField/DateTimeField.
        # date_hierarchy = 'publication_year' # Uncomment if publication_year was a DateField

        # Optional: Order books by title by default.
        # ordering = ('title',)

    # Register the Book model with the custom BookAdmin class.
    # This tells Django to use our custom configurations when displaying
    # the Book model in the admin interface.
admin.site.register(Book, BookAdmin)
    