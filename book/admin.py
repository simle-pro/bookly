from django.contrib import admin
from .models import (
    Profile, Book, Chapter, Rating, Comment,
    BookmarkList, Bookmark, Notification,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'created_at']
    list_filter = ['genre', 'created_at']
    search_fields = ['title', 'author__username']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'number']
    list_filter = ['book']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'value']
    list_filter = ['value']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'text', 'created_at']
    list_filter = ['created_at']


@admin.register(BookmarkList)
class BookmarkListAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['list', 'book', 'created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'text', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
