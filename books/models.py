from django.db import models
from django.contrib.auth.models import User


# --------------------------------
# Book Model
# --------------------------------

class Book(models.Model):

    title = models.CharField(
        max_length=200
    )

    author = models.CharField(
        max_length=150
    )

    genre = models.CharField(
        max_length=100
    )

    description = models.TextField()

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0
    )

    language = models.CharField(
        max_length=50,
        default="English"
    )

    publication_year = models.IntegerField()

    cover_image = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.title


# --------------------------------
# User Profile Model
# --------------------------------

class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    favorite_genre = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.user.username


# --------------------------------
# User Rating Model
# --------------------------------

class UserRating(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.book.title} - "
            f"{self.rating}"
        )


# --------------------------------
# Favorite Book Model
# --------------------------------

class FavoriteBook(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'user',
            'book',
        )

    def __str__(self):

        return (
            f"{self.user.username} - "
            f"{self.book.title}"
        )