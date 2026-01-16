from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'


def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'


def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")




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
