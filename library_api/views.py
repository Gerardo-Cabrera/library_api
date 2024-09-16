from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q, Max
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, Author, Favorite
from .serializers import BookSerializer, AuthorSerializer, FavoriteSerializer, RegisterSerializer
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError


# Authors and books
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'authors', 'book_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        # Overriding this method to use 'book_id' instead of 'id' in the URL.
        book_id = self.kwargs.get('pk')
        return self.queryset.get(book_id=book_id)

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                # Get the current maximum value of book_id
                max_book_id = Book.objects.aggregate(max_id=Max('book_id'))['max_id']
                if max_book_id is None:
                    max_book_id = 0

                # Increase the value
                new_book_id = str(int(max_book_id) + 1)
                while Book.objects.filter(book_id=new_book_id).exists():
                    new_book_id = str(int(new_book_id) + 1)

                # Add the new book_id to the book before saving
                serializer.save(book_id=new_book_id)
        except IntegrityError as e:
            raise ValidationError(f"Integrity error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"An error occurred: {str(e)}")
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Book added successfully!", "data": response.data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Book updated successfully!", "data": response.data}, status=status.HTTP_200_OK)
        
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Book deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'author_id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        # Overriding this method to use 'author_id' instead of 'id' in the URL.
        author_id = self.kwargs.get('pk')
        return self.queryset.get(author_id=author_id)

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                # Get the current maximum value of author_id
                max_author_id = Author.objects.aggregate(max_id=Max('author_id'))['max_id']
                if max_author_id is None:
                    max_author_id = 0

                # Increase the value
                new_author_id = str(int(max_author_id) + 1)
                while Author.objects.filter(author_id=new_author_id).exists():
                    new_author_id = str(int(new_author_id) + 1)

                # Add the new author_id to the author before saving
                serializer.save(author_id=new_author_id)
        except IntegrityError as e:
            raise ValidationError(f"Integrity error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"An error occurred: {str(e)}")
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Author added successfully!", "data": response.data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Author updated successfully!", "data": response.data}, status=status.HTTP_200_OK)
        
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Author deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

# Favorites
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites(request):
    try:
        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    if Favorite.objects.filter(user=request.user).count() >= 20:
         return Response({"detail": "Favorites limit reached"}, status=status.HTTP_400_BAD_REQUEST)
    
    _, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if not created:
        return Response({"detail": "Book is already in your favorites"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "Book added to favorites"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)


# Recommended
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_books(request):
    recommendations = recommend_books(request.user)
    serializer = BookSerializer(recommendations, many=True)
    return Response(serializer.data)

def recommend_books(user):
    favorite_books = Favorite.objects.filter(user=user).values_list('book', flat=True)
    favorite_books_objects = Book.objects.filter(id__in=favorite_books).select_related('authors')
    favorite_authors = Author.objects.filter(books__in=favorite_books_objects).distinct()
    related_books = Book.objects.filter(
        authors__in=favorite_authors
    ).exclude(id__in=favorite_books).distinct('id')[:5]

    return related_books

# Register and Login
@api_view(['POST'])
@permission_classes([AllowAny]) 
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny]) 
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        })
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
