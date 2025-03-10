from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Book

class UserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "john@example.com",
            "firstname": "John",
            "lastname": "Doe"
        }

    def test_create_user(self):
        """
        Test creating a new user.
        """
        url = reverse('user-create')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_list_users(self):
        """
        Test listing all users.
        """
        self.user = User.objects.create(**self.user_data)
        url = reverse('enrolled-users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  

class BookViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "publisher": "Test Publisher",
            "category": "Test Category"
        }
        self.book = Book.objects.create(**self.book_data)

    def test_list_available_books(self):
        """
        Test listing all available books.
        """
        url = reverse('books-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_book(self):
        """
        Test retrieving a single book by its ID.
        """
        url = reverse('book-retrieve', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    
    def test_borrow_book(self):
        """
        Test borrowing a book.
        """
        user = User.objects.create(email="borrower@example.com", firstname="Jane", lastname="Doe")
        url = reverse('borrow-book', args=[self.book.id])
        borrow_data = {
            "email": user.email,
            "duration_days": 7
        }
        response = self.client.post(url, borrow_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertFalse(self.book.available)
        self.assertEqual(self.book.borrowed_by, user)
 
class UserWithBooksViewTests(TestCase):
    def setUp(self):
    
        self.client = APIClient()
        self.user = User.objects.create(email="test@example.com", firstname="John", lastname="Doe")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            category="Test Category",
            available=False,
            borrowed_by=self.user
        )

    def test_list_users_with_books(self):
        """
        Test listing users with their borrowed books.
        """
        url = reverse('users-with-books-list')
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only one user exists from setUp
        self.assertEqual(len(response.data['results'][0]['borrowed_books']), 1)  # Only one book is borrowed by the user    