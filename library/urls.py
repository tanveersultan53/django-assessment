from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, AddFavoriteBookView, RemoveFavoriteBookView, FavoriteBooksView

router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
urlpatterns = [
    path('favorites/add/<int:book_id>', AddFavoriteBookView.as_view(), name='add_favorite_book'),
    path('favorites/remove/<int:book_id>', RemoveFavoriteBookView.as_view(), name='remove_favorite_book'),
    path('favorites', FavoriteBooksView.as_view(), name='favorite_books'),
    path('', include(router.urls)),
]
