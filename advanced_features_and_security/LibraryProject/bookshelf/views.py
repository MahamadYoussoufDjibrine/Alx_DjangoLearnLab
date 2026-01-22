from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required


@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    return HttpResponse("Book creation allowed")


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    return HttpResponse("Book editing allowed")


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    return HttpResponse("Book deletion allowed")


@permission_required("bookshelf.can_view", raise_exception=True)
def view_books(request):
    return HttpResponse("Book viewing allowed")
