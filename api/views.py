from .models import User, Book
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework import generics
from .pagination import PageSizePagination
from .serializers import UserSerializer, BookSerializer, BorrowBookInputSerializer, UserWithBooksSerializer, BorrowedBookSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# filter books by publisher, category 
class AvailableBookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=True)
    serializer_class = BookSerializer
    pagination_class = PageSizePagination
    filterset_fields = ('publisher','category')

class UnAvailableBookListView(generics.ListAPIView):
    queryset = Book.objects.filter(available=False)
    serializer_class = BorrowedBookSerializer

class BookRetrieveView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowBookView(APIView):
    def post(self, request, book_id):      

        input_serializer = BorrowBookInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(id=book_id, available=True)
        except Book.DoesNotExist:
            return Response({"error": "Book not available."}, status=status.HTTP_404_NOT_FOUND)

    
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

      
        # Update the book's availability and set the return date
        book.available = False
        book.borrowed_by = user
        book.return_date = (timezone.now() + timezone.timedelta(days=data['duration_days'])).date()
        book.save()

        # Return the updated book details
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserWithBooksListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserWithBooksSerializer