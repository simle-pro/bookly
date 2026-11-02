from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Profile(models.Model):
    ROLE_CHOICES = [
        ('author', 'Автор'),
        ('reader', 'Читатель'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    @property
    def is_author(self):
        return self.role == 'author'


class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)
    cover = models.FileField(upload_to='covers/', blank=True, null=True)
    audio = models.FileField(upload_to='audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        result = self.ratings.aggregate(avg=Avg('value'))['avg']
        return round(result, 1) if result else None

    @property
    def rating_count(self):
        return self.ratings.count()


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    number = models.PositiveIntegerField(default=1)
    text = models.TextField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f'{self.book.title} - {self.title}'


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(default=5)

    class Meta:
        unique_together = ['book', 'user']

    def __str__(self):
        return f'{self.book.title}: {self.user.username} = {self.value}'


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.book.title} - {self.user.username}'


class BookmarkList(models.Model):
    """Список закладок пользователя (напр. «Читаю», «Прочитано» или свой)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark_lists')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'name']
        ordering = ['name']

    def __str__(self):
        return f'{self.user.username}: {self.name}'


class Bookmark(models.Model):
    list = models.ForeignKey(BookmarkList, on_delete=models.CASCADE, related_name='bookmarks')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['list', 'book']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.list.name}: {self.book.title}'


class Notification(models.Model):
    """Сообщение: «вышла новая глава» — для тех, у кого книга в закладках."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notifications')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='notifications')
    text = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.text}'
