from django.contrib import admin
from .models import Library, Book, Author, Librarian, UserProfile


admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Librarian)
admin.site.register(UserProfile)
