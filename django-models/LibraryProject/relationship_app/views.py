from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book


# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(
        request,
        "relationship_app/list_books.html",
        {"books": books}
    )


# Class-based view: display details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_object(self):
        library_id = self.kwargs.get("library_id")
        return get_object_or_404(Library, id=library_id)
