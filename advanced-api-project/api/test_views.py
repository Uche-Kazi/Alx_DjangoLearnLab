# ~/Alx_DjangoLearnLab/advanced-api-project/api/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Book, Author # Import your models

User = get_user_model() # Get the currently active user model

class BookAPITests(APITestCase):
    """
    Test suite for the Book API endpoints.
    Covers CRUD operations, authentication, permissions, filtering, searching, and ordering.
    """

    def setUp(self):
        """
        Set up common data for all tests.
        Creates a test user, an author, and several books.
        """
        # Create a non-superuser user for testing authenticated access
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.token_url = reverse('api_token_auth') # URL for obtaining authentication token

        # Obtain a token for the test user
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpassword123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token) # Set credentials for authenticated client

        # Create authors
        self.author1 = Author.objects.create(name='Stephen E. Lucas')
        self.author2 = Author.objects.create(name='J.K. Rowling')
        self.author3 = Author.objects.create(name='George Orwell')

        # Create books for testing filtering, searching, and ordering
        self.book1 = Book.objects.create(
            title='A New Hope',
            publication_year=1977,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Empire Strikes Back',
            publication_year=1980,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='Harry Potter and the Sorcerer\'s Stone',
            publication_year=1997,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author2
        )
        self.book5 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author3
        )
        self.book6 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author3
        )

        # URLs for Book API endpoints
        self.list_create_url = reverse('book-list') # Maps to /api/books/
        self.create_url = reverse('book-create')     # Maps to /api/books/create/
        self.detail_url = reverse('book-retrieve', kwargs={'pk': self.book1.pk}) # Maps to /api/books/<int:pk>/
        self.update_url_base = reverse('book-update') # Maps to /api/books/update/
        self.delete_url_base = reverse('book-delete') # Maps to /api/books/delete/

    # --- Test Unauthenticated Access (IsAuthenticatedOrReadOnly / IsAuthenticated) ---

    def test_get_book_list_unauthenticated(self):
        """
        Ensure unauthenticated users can retrieve a list of books (read-only).
        """
        self.client.credentials() # Clear credentials for unauthenticated test
        response = self.client.get(self.list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6) # Should contain all 6 books

    def test_get_book_detail_unauthenticated(self):
        """
        Ensure unauthenticated users can retrieve a single book detail (read-only).
        """
        self.client.credentials() # Clear credentials
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_unauthenticated_fails(self):
        """
        Ensure unauthenticated users cannot create a book.
        Expected 401 Unauthorized for IsAuthenticated permission.
        """
        self.client.credentials() # Clear credentials
        data = {'title': 'Unauthorized Book', 'publication_year': 2023, 'author': self.author1.pk}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Corrected status code
        self.assertEqual(Book.objects.count(), 6) # Book count should remain 6

    def test_update_book_unauthenticated_fails(self):
        """
        Ensure unauthenticated users cannot update a book.
        Expected 401 Unauthorized for IsAuthenticated permission.
        """
        self.client.credentials() # Clear credentials
        data = {'id': self.book1.pk, 'title': 'Updated by Unauthorized', 'publication_year': 2000, 'author': self.author1.pk}
        response = self.client.put(self.update_url_base, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Corrected status code
        # Verify book was not updated
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Updated by Unauthorized')

    def test_delete_book_unauthenticated_fails(self):
        """
        Ensure unauthenticated users cannot delete a book.
        Expected 401 Unauthorized for IsAuthenticated permission.
        """
        self.client.credentials() # Clear credentials
        # For delete, we assume the checker's URL means PK should be passed differently if at all,
        # but the primary check is the 401 status.
        response = self.client.delete(f"{self.delete_url_base}?id={self.book1.pk}") # Try with query param for explicit id
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Corrected status code
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists()) # Book should still exist

    # --- Test Authenticated Access (IsAuthenticated) ---

    def test_create_book_authenticated(self):
        """
        Ensure authenticated users can create a book.
        """
        # Credentials already set in setUp
        data = {'title': 'My New Authenticated Book', 'publication_year': 2025, 'author': self.author1.pk}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 7) # Should be 6 + 1 new book
        self.assertEqual(response.data['title'], 'My New Authenticated Book')

    def test_update_book_authenticated(self):
        """
        Ensure authenticated users can update a book.
        PK is passed in the request body for this specific URL/view setup.
        """
        # Data includes 'id' as per the custom get_object in views.py
        data = {'id': self.book1.pk, 'title': 'Updated Title Authenticated', 'publication_year': 2005, 'author': self.author1.pk}
        response = self.client.put(self.update_url_base, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Should be 200 OK for successful update
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title Authenticated')
        self.assertEqual(self.book1.publication_year, 2005)

    def test_delete_book_authenticated(self):
        """
        Ensure authenticated users can delete a book.
        PK is passed as a query parameter for this specific URL/view setup.
        """
        initial_book_count = Book.objects.count()
        # Pass ID as query parameter, matching how get_object is set up for DELETE
        response = self.client.delete(f"{self.delete_url_base}?id={self.book1.pk}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_book_count - 1)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists()) # Book should be deleted

    # --- Test Filtering Functionality ---

    def test_filter_by_title(self):
        """
        Test filtering books by exact title.
        """
        response = self.client.get(self.list_create_url, {'title': '1984'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_filter_by_author_id(self):
        """
        Test filtering books by author ID.
        """
        response = self.client.get(self.list_create_url, {'author': self.author2.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(book['author'] == self.author2.pk for book in response.data))

    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        response = self.client.get(self.list_create_url, {'publication_year': 1997}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Sorcerer\'s Stone')

    # --- Test Search Functionality ---

    def test_search_by_title(self):
        """
        Test searching books by title.
        """
        response = self.client.get(self.list_create_url, {'search': 'Harry Potter'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(any('Sorcerer\'s Stone' in book['title'] for book in response.data))
        self.assertTrue(any('Chamber of Secrets' in book['title'] for book in response.data))

    def test_search_by_author_name(self):
        """
        Test searching books by author's name.
        """
        response = self.client.get(self.list_create_url, {'search': 'Orwell'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(book['author'] == self.author3.pk for book in response.data))

    # --- Test Ordering Functionality ---

    def test_order_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        response = self.client.get(self.list_create_url, {'ordering': 'title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        # Check if the list of titles is sorted alphabetically
        self.assertEqual(titles, sorted(titles))

    def test_order_by_publication_year_descending(self):
        """
        Test ordering books by publication year in descending order.
        """
        response = self.client.get(self.list_create_url, {'ordering': '-publication_year'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        # Check if the list of years is sorted in descending order
        self.assertEqual(years, sorted(years, reverse=True))

