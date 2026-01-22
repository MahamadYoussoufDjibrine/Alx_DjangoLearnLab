# relationship_app/test_data.py
from .models import Author, Book, Library, Librarian

def create_sample_data():
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Harper Lee")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter", author=author1)
    book2 = Book.objects.create(title="1984", author=author2)
    book3 = Book.objects.create(title="Animal Farm", author=author2)
    book4 = Book.objects.create(title="To Kill a Mockingbird", author=author3)
    
    # Create libraries
    library1 = Library.objects.create(name="City Central Library")
    library2 = Library.objects.create(name="University Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book4)
    library2.books.add(book2, book3)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Alice Smith", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Johnson", library=library2)
    
    print("Sample data created successfully!")
    print(f"Authors: {Author.objects.count()}")
    print(f"Books: {Book.objects.count()}")
    print(f"Libraries: {Library.objects.count()}")
    print(f"Librarians: {Librarian.objects.count()}")