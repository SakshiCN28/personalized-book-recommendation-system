from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'genre',
        'rating',
        'language',
        'publication_year',
    )

    search_fields = (
        'title',
        'author',
        'genre',
    )

    list_filter = (
        'genre',
        'language',
    )