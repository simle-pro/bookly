from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('lang/<str:lang>/', views.set_lang, name='set_lang'),

    path('profile/', views.profile, name='profile'),

    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('bookmarks/list/<int:list_id>/delete/',
         views.bookmark_list_delete, name='bookmark_list_delete'),
    path('bookmarks/add/<int:book_id>/', views.bookmark_add, name='bookmark_add'),
    path('bookmarks/<int:bookmark_id>/remove/',
         views.bookmark_remove, name='bookmark_remove'),

    path('notifications/', views.notifications, name='notifications'),

    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/read/', views.book_read, name='book_read'),
    path('book/<int:book_id>/listen/', views.book_listen, name='book_listen'),
    path('book/<int:book_id>/rate/', views.book_rate, name='book_rate'),
    path('book/<int:book_id>/comment/', views.book_comment, name='book_comment'),

    path('author/', views.author_books, name='author_books'),
    path('author/book/add/', views.book_add, name='book_add'),
    path('author/book/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('author/book/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('author/book/<int:book_id>/chapter/add/', views.chapter_add, name='chapter_add'),
    path('author/book/<int:book_id>/chapter/<int:chapter_id>/delete/',
         views.chapter_delete, name='chapter_delete'),
]
