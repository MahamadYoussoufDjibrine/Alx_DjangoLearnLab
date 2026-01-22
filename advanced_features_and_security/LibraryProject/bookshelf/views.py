from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.can_create", raise_exception=True)
def example_form_view(request):
    form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})
