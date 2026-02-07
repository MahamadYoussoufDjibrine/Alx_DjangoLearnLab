from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Book
from .serializers import BookSerializer


class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Task 2: filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filtering (query params): ?title=...&publication_year=...&author=...
    filterset_fields = ['title', 'publication_year', 'author']

    # Searching (query param): ?search=...
    # Allow searching by book title and author's name
    search_fields = ['title', 'author__name']

    # Ordering (query param): ?ordering=title or ?ordering=-publication_year
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['title']
