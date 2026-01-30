from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Task 1 endpoint
    path('books/', BookList.as_view(), name='book-list'),

    # Task 2 router endpoints
    path('', include(router.urls)),
]
