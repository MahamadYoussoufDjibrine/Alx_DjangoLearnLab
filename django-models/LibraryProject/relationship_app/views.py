# relationship_app/views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library, Author


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_object(self):
        # Get the library by ID from URL
        library_id = self.kwargs.get('library_id')
        return get_object_or_404(Library, id=library_id)