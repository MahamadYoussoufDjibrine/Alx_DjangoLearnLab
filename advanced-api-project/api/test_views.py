from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from api.models import Author, Book


class BookAPITestCase(TestCase):
    """
    Tests for:
    - CRUD endpoints (list, detail, create, update, delete)
    - Permissions (public read, authenticated write)
    - Filtering, searching, ordering on the list endpoint
    """

    def setUp(self):
        self.client = APIClient()

        # Users
        self.user = User.objects.create_user(username="user1", password="pass12345")

        # Authors
        self.author1 = Author.objects.create(name="Chimamanda Ngozi Adichie")
        self.author2 = Author.objects.create(name="Ngugi wa Thiong'o")

        # Books
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

        # Endpoints (match your api/urls.py)
        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book1.id}/"
        self.create_url = "/api/books/create/"
        self.update_url = f"/api/books/update/{self.book1.id}/"
        self.delete_url = f"/api/books/delete/{self.book1.id}/"

    # -------------------------
    # Public READ endpoints
    # -------------------------
    def test_list_books_public(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Ensure list returns at least the seeded books
        self.assertTrue(len(res.data) >= 3)

    def test_detail_book_public(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.book1.id)
        self.assertEqual(res.data["title"], self.book1.title)

    # -------------------------
    # Auth required WRITE endpoints
    # -------------------------
    def test_create_book_requires_auth(self):
        payload = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertIn(res.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id
        }
        res = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["title"], "New Book")
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_update_book_requires_auth(self):
        payload = {
            "title": "Updated Title",
            "publication_year": self.book1.publication_year,
            "author": self.author1.id
        }
        res = self.client.put(self.update_url, payload, format="json")
        self.assertIn(res.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_update_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Updated Title",
            "publication_year": self.book1.publication_year,
            "author": self.author1.id
        }
        res = self.client.put(self.update_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book_requires_auth(self):
        res = self.client.delete(self.delete_url)
        self.assertIn(res.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(self.delete_url)
        # DRF destroy may return 204 or 200 depending on configuration
        self.assertIn(res.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # -------------------------
    # Filtering / Searching / Ordering
    # -------------------------
    def test_filter_by_publication_year(self):
        res = self.client.get(self.list_url + "?publication_year=2006")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        returned_ids = [b["id"] for b in res.data]
        self.assertIn(self.book2.id, returned_ids)
        self.assertNotIn(self.book1.id, returned_ids)

    def test_filter_by_author(self):
        res = self.client.get(self.list_url + f"?author={self.author2.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        returned_ids = [b["id"] for b in res.data]
        self.assertIn(self.book3.id, returned_ids)
        self.assertNotIn(self.book2.id, returned_ids)

    def test_search_by_title(self):
        res = self.client.get(self.list_url + "?search=Purple")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertIn("Purple Hibiscus", titles)

    def test_search_by_author_name(self):
        res = self.client.get(self.list_url + "?search=Chimamanda")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        returned_ids = [b["id"] for b in res.data]
        self.assertIn(self.book1.id, returned_ids)
        self.assertIn(self.book2.id, returned_ids)

    def test_ordering_by_publication_year_desc(self):
        res = self.client.get(self.list_url + "?ordering=-publication_year")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in res.data]
        self.assertEqual(years, sorted(years, reverse=True))
