from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Author, Book


class BookAPITestCase(TestCase):
    """
    Unit tests for the Book API endpoints in advanced-api-project.

    Coverage:
    - CRUD operations (list, detail, create, update, delete)
    - Permissions (public read, authenticated write)
    - Filtering, searching, ordering on ListView
    """

    def setUp(self):
        self.client = APIClient()

        # Create a normal authenticated user for write operations
        self.user = User.objects.create_user(username="user1", password="pass12345")

        # Create authors
        self.author1 = Author.objects.create(name="Chimamanda Ngozi Adichie")
        self.author2 = Author.objects.create(name="Ngugi wa Thiong'o")

        # Create books
        self.book1 = Book.objects.create(
            title="Purple Hibiscus",
            publication_year=2003,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Half of a Yellow Sun",
            publication_year=2006,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="The River Between",
            publication_year=1965,
            author=self.author2
        )

        # Endpoints (must match api/urls.py)
        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book1.id}/"
        self.create_url = "/api/books/create/"
        self.update_url = f"/api/books/update/{self.book1.id}/"
        self.delete_url = f"/api/books/delete/{self.book1.id}/"

    # -------------------------
    # Public READ endpoints
    # -------------------------
    def test_list_books_public_returns_200(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure response has data and includes our seeded books
        self.assertTrue(len(response.data) >= 3)  # <-- required: response.data

    def test_detail_book_public_returns_200_and_correct_data(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book1.id)  # <-- required: response.data
        self.assertEqual(response.data["title"], self.book1.title)

    # -------------------------
    # WRITE endpoints require authentication
    # -------------------------
    def test_create_book_unauthenticated_denied(self):
        payload = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id,
        }
        response = self.client.post(self.create_url, payload, format="json")
        # Depending on auth config, could be 401 or 403
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_book_authenticated_returns_201(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id,
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")  # <-- required: response.data
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_update_book_unauthenticated_denied(self):
        payload = {
            "title": "Updated Title",
            "publication_year": self.book1.publication_year,
            "author": self.author1.id,
        }
        response = self.client.put(self.update_url, payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_update_book_authenticated_returns_200_and_updates_db(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Updated Title",
            "publication_year": self.book1.publication_year,
            "author": self.author1.id,
        }
        response = self.client.put(self.update_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")  # <-- required: response.data
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book_unauthenticated_denied(self):
        response = self.client.delete(self.delete_url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_authenticated_returns_204_or_200_and_deletes(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        # DRF DestroyAPIView typically returns 204
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # -------------------------
    # Filtering / Searching / Ordering on ListView
    # -------------------------
    def test_filter_by_publication_year(self):
        response = self.client.get(self.list_url + "?publication_year=2006")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [b["id"] for b in response.data]  # <-- response.data
        self.assertIn(self.book2.id, returned_ids)
        self.assertNotIn(self.book1.id, returned_ids)

    def test_filter_by_author(self):
        response = self.client.get(self.list_url + f"?author={self.author2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [b["id"] for b in response.data]  # <-- response.data
        self.assertIn(self.book3.id, returned_ids)
        self.assertNotIn(self.book2.id, returned_ids)

    def test_search_by_title(self):
        response = self.client.get(self.list_url + "?search=Purple")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]  # <-- response.data
        self.assertIn("Purple Hibiscus", titles)

    def test_search_by_author_name(self):
        response = self.client.get(self.list_url + "?search=Chimamanda")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [b["id"] for b in response.data]  # <-- response.data
        self.assertIn(self.book1.id, returned_ids)
        self.assertIn(self.book2.id, returned_ids)

    def test_ordering_by_publication_year_desc(self):
        response = self.client.get(self.list_url + "?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]  # <-- response.data
        self.assertEqual(years, sorted(years, reverse=True))
