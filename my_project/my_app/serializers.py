# ~/Alx_DjangoLearnLab/my_project/my_app/serializers.py

from rest_framework import serializers
from .models import Book # Import your Book model

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book model instances to JSON (and vice-versa) for the API.
    """
    class Meta:
        model = Book
        fields = '__all__' # Includes all fields from the Book model

