# relationship_app/urls.py
from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # URL for function-based view (lists all books)
    path('books/', views.list_books, name='list_books'),
    
    # URL for class-based view (shows specific library details)
    path('library/<int:library_id>/', views.LibraryDetailView.as_view(), name='library_detail'),
]