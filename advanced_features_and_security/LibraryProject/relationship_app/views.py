from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponse


# Role-based access decorators
def admin_required(view_func):
    return user_passes_test(lambda u: u.role == "Admin")(view_func)


def librarian_required(view_func):
    return user_passes_test(lambda u: u.role == "Librarian")(view_func)


def member_required(view_func):
    return user_passes_test(lambda u: u.role == "Member")(view_func)


@admin_required
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@librarian_required
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@member_required
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Library detail view
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_object(self):
        library_id = self.kwargs.get("library_id")
        return get_object_or_404(Library, id=library_id)


# User login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("relationship_app:list_books")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


# User logout view
def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


# User registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("relationship_app:login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Book management views with permissions
@permission_required('relationship_app.add_book', raise_exception=True)
def add_book(request):
    return HttpResponse("Add book view - permission granted")


@permission_required('relationship_app.change_book', raise_exception=True)
def edit_book(request, book_id):
    return HttpResponse("Edit book view - permission granted")


@permission_required('relationship_app.delete_book', raise_exception=True)
def delete_book(request, book_id):
    return HttpResponse("Delete book view - permission granted")
