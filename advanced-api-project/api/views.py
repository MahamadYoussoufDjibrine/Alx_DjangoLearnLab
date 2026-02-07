from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# ListView: Public (unauthenticated users can read)
# GET /api/books/
class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


# DetailView: Public (unauthenticated users can read)
# GET /api/books/<pk>/
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


# CreateView: Auth required (only logged-in users can create)
# POST /api/books/create/
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Customize behavior: ensure serializer validation runs and return created object.
    # (DRF already does this; this override just makes behavior explicit for the task.)
    def perform_create(self, serializer):
        serializer.save()


# UpdateView: Auth required (only logged-in users can update)
# PUT/PATCH /api/books/update/<pk>/
class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Customize behavior: serializer validation will run (e.g., publication_year not future).
    def perform_update(self, serializer):
        serializer.save()


# DeleteView: Auth required (only logged-in users can delete)
# DELETE /api/books/delete/<pk>/
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
