from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    author_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    about = models.TextField(blank=True)
    ratings_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    text_reviews_count = models.IntegerField(default=0)
    works_count = models.IntegerField(default=0)
    fans_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    book_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=500)
    authors = models.ManyToManyField(Author, related_name='books')
    work_id = models.CharField(max_length=50, blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True)
    isbn13 = models.CharField(max_length=13, blank=True, null=True)
    asin = models.CharField(max_length=10, blank=True, null=True)
    language = models.CharField(max_length=10)
    average_rating = models.FloatField(default=0, null=True)
    ratings_count = models.IntegerField(default=0, null=True)
    text_reviews_count = models.IntegerField(default=0, null=True)
    publication_date = models.CharField(max_length=20, blank=True, null=True)
    original_publication_date = models.CharField(max_length=20, blank=True, null=True)
    format = models.CharField(max_length=50, blank=True, null=True)
    edition_information = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    series_name = models.CharField(max_length=255, blank=True, null=True)
    series_position = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]

class Favorite(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_favorite')
        ]
        indexes = [
            models.Index(fields=['user', 'book']),
        ]
