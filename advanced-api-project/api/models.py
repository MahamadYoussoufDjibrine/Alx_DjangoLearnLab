from django.db import models

# Author represents a writer who can have many books (one-to-many relationship).
# One Author -> Many Book records via the Book.author foreign key.
class Author(models.Model):
    # Stores the author's full name.
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book represents a published work written by exactly one Author.
# The 'author' field is a ForeignKey, so multiple books can reference the same author.
class Book(models.Model):
    # Stores the book title.
    title = models.CharField(max_length=255)

    # Stores the year the book was published (integer for easy validation/querying).
    publication_year = models.IntegerField()

    # Links each book to one author. If an author is deleted, their books are deleted too.
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
