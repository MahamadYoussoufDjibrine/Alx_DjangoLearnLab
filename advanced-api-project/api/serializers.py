from datetime import date
from rest_framework import serializers
from .models import Author, Book

# BookSerializer converts Book model instances into JSON (and validates input JSON).
# It serializes all fields on the Book model.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation: publication_year must not be in the future.
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future.")
        return value


# AuthorSerializer includes the author's name AND a nested list of related books.
# The relationship is handled via Book.author ForeignKey and the related_name='books'.
# By setting many=True, we serialize multiple books for the same author.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
