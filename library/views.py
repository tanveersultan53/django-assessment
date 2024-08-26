from rest_framework import viewsets,filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import UserProfile
from .models import Book, Author
from rest_framework.response import Response
from .paginations import DefaultPagination
from .recommendations import get_book_recommendations
from .serializers import BookSerializer, AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = DefaultPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__first_name', 'author__last_name']

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class AddFavoriteBookView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        user_profile = request.user.profile
        book = Book.objects.get(id=book_id)

        if user_profile.favorite_books.count() >= 20:
            return Response({"message": "You can only have 20 favorite books."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.favorite_books.add(book)
        user_profile.save()

        # recommended_books = get_book_recommendations(request.user)
        # serializer = BookSerializer(recommended_books, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("book marked favorite successfully", status=status.HTTP_200_OK)


class RemoveFavoriteBookView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        user_profile = request.user.profile
        book = Book.objects


class FavoriteBooksView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get(self, request, format=None):
        try:
            # Retrieve the user's profile
            user_profile = request.user.profile

            # Get all favorite books
            favorite_books = user_profile.favorite_books.all()

            # Serialize the favorite books
            serializer = self.serializer_class(favorite_books, many=True)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)