# LibraryProject/relationship_app/admin.py

from django.contrib import admin
# No CustomUser or UserAdmin imports here anymore.
from .models import Author, Book, Library, Librarian, Loan # CustomUser is NOT in this import line

# Register your other models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(Loan)

# The CustomUserAdmin class and its @admin.register(CustomUser) decorator
# should NOT be in this file anymore.
# It has been moved to LibraryProject/bookshelf/admin.py.
# Ensure there is NO code below this line related to CustomUserAdmin in this file.
