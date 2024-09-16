from rest_framework import serializers
from .models import Author, Book, Favorite
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['author_id', 'name', 'gender', 'image_url', 'about', 'ratings_count', 'average_rating', 'text_reviews_count', 'works_count', 'fans_count']
        read_only_fields = ['author_id']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['book_id']

class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = Favorite
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user