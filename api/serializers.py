# ~/Alx_DjangoLearnLab/api/serializers.py

from rest_framework import serializers
from .models import Author, Book # Import your models
from datetime import date # Import date for validation

# Define BookSerializer first, as AuthorSerializer will nest it.
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Includes custom validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = '__all__' # Include all fields from the Book model

    def validate_publication_year(self, value):
        """
        Custom validation for the 'publication_year' field.
        Ensures the publication year is not in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes a nested BookSerializer to show books related to the author.
    """
    # Use many=True to indicate that an Author can have multiple books.
    # read_only=True means these books won't be editable when updating an Author directly,
    # and they won't be required during Author creation.
    # This is a common pattern for nested read operations.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books'] # Include 'books' for the nested serialization

