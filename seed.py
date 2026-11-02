"""Демо-данные: запускать через  .venv/bin/python manage.py shell < seed.py"""
import shutil
from pathlib import Path
from django.contrib.auth.models import User
from book.models import Profile, Book, Chapter, Rating, Comment

# ---- users ----
author, created = User.objects.get_or_create(
    username='author', defaults={'first_name': 'Иван', 'last_name': 'Авторов'})
if created:
    author.set_password('author123')
    author.save()
Profile.objects.get_or_create(user=author, defaults={'role': 'author'})
# сигнал мог уже создать профиль с ролью reader — поправляем
Profile.objects.filter(user=author).update(role='author')

readers = []
for name in ('olga', 'petr'):
    u, cr = User.objects.get_or_create(username=name)
    if cr:
        u.set_password('reader123')
        u.save()
    Profile.objects.get_or_create(user=u, defaults={'role': 'reader'})
    readers.append(u)

# ---- books ----
books_data = [
    {
        'title': 'Тайна старого замка',
        'genre': 'Детектив',
        'description': 'Молодой следователь прибывает в провинциальный город, '
                       'чтобы расследовать исчезновение владельца древнего замка. '
                       'Каждая улика ведёт к неожиданному выводу.',
        'audio': True,
        'chapters': [
            ('Глава 1. Прибытие',
             'Поезд прибыл в маленькую станцию под вечер.\n'
             'Следователь Морозов вышел на перрон и сразу почувствовал запах старости — '
             'верно, город жил прошлым.\n'
             'Из тумана вышла карета, и кучер молча кивнул ему.'),
            ('Глава 2. Первый улика',
             'В замке его встретила экономка с мрачным лицом.\n'
             '— Здесь всё как было, — сказала она. — Ничего не трогали.\n'
             'Но на полу лежала свежая спичка, а хозяин не курил двадцать лет.'),
            ('Глава 3. Разгадка',
             'К вечеру всё встало на свои места.\n'
             'Спичка принадлежала кучеру, а карета уезжала каждую ночь без хозяина.\n'
             'Морозов улыбнулся: преступление всегда простое, пока в него не поверят.'),
        ],
    },
    {
        'title': 'Звёздный путник',
        'genre': 'Фантастика',
        'description': 'Экипаж исследовательского корабля находит сигнал, '
                       'которому нет объяснения. Путь к его источнику меняет всё, '
                       'что они знали о вселенной.',
        'audio': False,
        'chapters': [
            ('Глава 1. Сигнал',
             'Радиотелескоп поймал повторяющийся импульс.\n'
             'Он шёл из области, где по картам не было ничего — ни звёзд, ни пыли.\n'
             'Команда решила проверить.'),
            ('Глава 2. Долгий полёт',
             'Год в гиперсне — и корабль вышел к чёрной пустоте.\n'
             'В центре пустоты висел объект размером с луну.\n'
             'Он не отражал свет, но излучал мысль.'),
            ('Глава 3. Контакт',
             '— Вы пришли, — сказал объект.\n'
             '— Мы пришли, — ответил капитан.\n'
             'И человечество впервые услышало, что Вселенная не молчит.'),
        ],
    },
    {
        'title': 'Дом на холме',
        'genre': 'Классика',
        'description': 'История семьи, которая вернулась в родовой дом, '
                       'чтобы начать всё заново. Тёплая книга о прошлом, '
                       'прощении и надежде.',
        'audio': False,
        'chapters': [
            ('Глава 1. Возвращение',
             'Дорога вилась вверх по холму, и с каждой вершиной дом становился ближе.\n'
             'Анна открыла ворота — они скрипнули, как двадцать лет назад.'),
            ('Глава 2. Старые письма',
             'В сундуке под лестницей она нашла письма отца.\n'
             'Они были написаны, но никогда не отправлены.\n'
             'Строки говорили о том, о чём молчали при жизни.'),
        ],
    },
]

for data in books_data:
    book, created = Book.objects.get_or_create(
        title=data['title'],
        defaults={
            'author': author,
            'description': data['description'],
            'genre': data['genre'],
        },
    )
    if created:
        for i, (title, text) in enumerate(data['chapters'], start=1):
            Chapter.objects.create(book=book, title=title, number=i, text=text)
        if data['audio']:
            src = Path('/tmp/demo_audio.mp3')
            if src.exists():
                dest = Path('media/audio') / f'demo_{book.id}.mp3'
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dest)
                book.audio.name = f'audio/demo_{book.id}.mp3'
                book.save()
        print(f'создана книга: {book.title}')

# ---- ratings ----
ratings = {
    'Тайна старого замка': {'olga': 5, 'petr': 4},
    'Звёздный путник': {'olga': 4, 'petr': 5},
    'Дом на холме': {'petr': 5},
}
for title, users in ratings.items():
    book = Book.objects.get(title=title)
    for uname, val in users.items():
        Rating.objects.update_or_create(
            book=book, user=User.objects.get(username=uname),
            defaults={'value': val})

# ---- comments ----
comments = [
    ('Тайна старого замка', 'olga', 'Очень захватывающая, читала за один вечер!'),
    ('Тайна старого замка', 'petr', 'Развязка неожиданная, но справедливая.'),
    ('Звёздный путник', 'petr', 'Классическая фантастира, понравился финал.'),
    ('Дом на холме', 'olga', 'Трогательная книга, перечитала дважды.'),
]
for title, uname, text in comments:
    book = Book.objects.get(title=title)
    user = User.objects.get(username=uname)
    if not Comment.objects.filter(book=book, user=user, text=text).exists():
        Comment.objects.create(book=book, user=user, text=text)

print('Готово! Книги:', Book.objects.count(),
      '| Оценки:', Rating.objects.count(),
      '| Комментарии:', Comment.objects.count())
print('Логины: author/author123, olga/reader123, petr/reader123')
