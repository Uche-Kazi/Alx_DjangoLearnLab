# ~/Alx_DjangoLearnLab/api_project/api/serializers.py

from rest_framework import serializers
from .models import Book # Import your Book model

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Converts Book model instances into JSON format for API responses.
    """
    class Meta:
        model = Book
        fields = '__all__' # Include all fields from the Book model

