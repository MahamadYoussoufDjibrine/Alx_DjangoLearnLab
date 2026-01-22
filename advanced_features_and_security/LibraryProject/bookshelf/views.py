from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import ExampleForm



@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    return HttpResponse("List of books")


@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    return HttpResponse("Create book")


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    return HttpResponse("Edit book")


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    return HttpResponse("Delete book")

@login_required
def book_list(request):
    form = ExampleForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("search_query")
        if query:
            # ORM usage prevents SQL injection
            books = books.filter(title__icontains=query)

    return render(request, "bookshelf/book_list.html", {
        "books": books,
        "form": form
    })

