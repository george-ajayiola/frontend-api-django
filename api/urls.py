from django.urls import path
from .views import UserCreateView, AvailableBookListView, BookRetrieveView, BorrowBookView, UserListView, UserWithBooksListView, UnAvailableBookListView

urlpatterns = [
    path('userCreate', UserCreateView.as_view(), name='user-create'),
    path('books', AvailableBookListView.as_view(), name='books-list'),
    path('book/<int:pk>', BookRetrieveView.as_view(), name='book-retrieve'),
    path('book/<int:book_id>/borrow', BorrowBookView.as_view(), name='borrow-book'),
    path('users/',UserListView.as_view(),name="enrolled-users"),
    path('users/books', UserWithBooksListView.as_view(), name='users-with-books-list'),
    path('books/borrowed',UnAvailableBookListView.as_view(),name='unavailable-books')
]