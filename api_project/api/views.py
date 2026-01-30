from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Task 1 view
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Task 2 viewset (CRUD)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
