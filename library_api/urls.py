from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, add_to_favorites, list_favorites, recommended_books, register, login

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('favorites/', list_favorites, name='list_favorites'),
    path('favorites/add/', add_to_favorites, name='add_to_favorites'),
    path('recommended-books/', recommended_books, name='recommended_books'),
]
