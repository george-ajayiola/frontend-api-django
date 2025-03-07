from rest_framework import serializers
from .models import User, Book

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname','lastname','email']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'category']

class BorrowBookInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    duration_days = serializers.IntegerField(min_value=1)


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'category','return_date']


class UserWithBooksSerializer(serializers.ModelSerializer):
    borrowed_books = BorrowedBookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname', 'borrowed_books']