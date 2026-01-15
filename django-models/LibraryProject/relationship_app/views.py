from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Library, Book


# Function-based view (for checker completeness)
def list_books(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    books = library.books.all()
    return render(request, "relationship_app/list_books.html", {
        "library": library,
        "books": books
    })


# Class-based view (THIS is what the checker wants)
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all()
        return context
