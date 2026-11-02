import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import *
from .translations import translate, get_lang


def tr(request, text, **kwargs):
    """Перевод строки по языку из cookie запроса."""
    return translate(get_lang(request), text, **kwargs)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, tr(request, 'Регистрация прошла успешно!'))
            return redirect('book_list')
    else:
        form = RegisterForm()
        form.fields['role'].choices = [
            (value, tr(request, label)) for value, label in form.fields['role'].choices
        ]
    return render(request, 'book/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_list')
        messages.error(request, tr(request, 'Неверный логин или пароль'))
    return render(request, 'book/login.html')


def user_logout(request):
    logout(request)
    return redirect('book_list')


def set_lang(request, lang):
    """Переключение языка: ставит cookie и возвращает назад."""
    if lang not in ('ru', 'en', 'de'):
        lang = 'ru'
    response = redirect(request.META.get('HTTP_REFERER') or 'book_list')
    response.set_cookie('lang', lang, max_age=365 * 24 * 3600)
    return response






def book_list(request):
    query = request.GET.get('q', '').strip()
    books = list(Book.objects.all())
    if query:
        needle = query.casefold()
        books = [
            b for b in books
            if needle in b.title.casefold() or needle in b.author.username.casefold()
        ]
    return render(request, 'book/book_list.html', {'books': books, 'query': query})





def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = book.comments.all()
    comment_form = CommentForm()
    comment_form.fields['text'].widget.attrs['placeholder'] = tr(request, 'Ваш комментарий...')
    rating_form = RatingForm()
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(book=book, user=request.user).first()
    return render(request, 'book/book_detail.html', {
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
    })


@login_required
def book_rate(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                book=book, user=request.user,
                defaults={'value': form.cleaned_data['value']},
            )
    return redirect('book_detail', book_id=book_id)


@login_required
def book_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
    return redirect('book_detail', book_id=book_id)



def book_read(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    chapters = list(book.chapters.all())
    if not chapters:
        return render(request, 'book/reader.html', {
            'book': book, 'chapter': None, 'chapters': [],
            'mode': 'chapters',
        })

    mode = request.GET.get('mode', 'chapters')
    if mode not in ('chapters', 'all'):
        mode = 'chapters'

    if mode == 'all':
        sections = [
            {
                'chapter': c,
                'paragraphs': [p for p in c.text.split('\n') if p.strip()],
            }
            for c in chapters
        ]
        return render(request, 'book/reader.html', {
            'book': book,
            'chapter': None,
            'chapters': chapters,
            'sections': sections,
            'mode': mode,
        })

    chapter_id = request.GET.get('chapter')
    if chapter_id:
        chapter = next((c for c in chapters if str(c.id) == str(chapter_id)), chapters[0])
    else:
        chapter = chapters[0]

    index = chapters.index(chapter)
    prev_chapter = chapters[index - 1] if index > 0 else None
    next_chapter = chapters[index + 1] if index < len(chapters) - 1 else None

    return render(request, 'book/reader.html', {
        'book': book,
        'chapter': chapter,
        'chapters': chapters,
        'paragraphs': [p for p in chapter.text.split('\n') if p.strip()],
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'mode': mode,
    })



def book_listen(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not book.audio:
        return redirect('book_detail', book_id=book_id)
    return render(request, 'book/player.html', {'book': book})



def _is_author(user):
    if not user.is_authenticated:
        return False
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'role': 'reader'})
    return profile.is_author


@login_required
def author_books(request):
    if not _is_author(request.user):
        messages.error(request, tr(request, 'Это кабинет только для авторов'))
        return redirect('book_list')
    books = Book.objects.filter(author=request.user)
    return render(request, 'book/author_books.html', {'books': books})


def _split_txt_to_chapters(text):
    """Режет txt по строкам-маркерам: 'Глава 1', '# ...'."""
    parts = re.split(r'^(?:Глава\s+\d+.*|#[^\n]*)\s*$', text, flags=re.MULTILINE)
    markers = re.findall(r'^(Глава\s+\d+.*|#[^\n]*)$', text, flags=re.MULTILINE)
    chapters = []
    if markers:
        for i, marker in enumerate(markers):
            title = marker.lstrip('#').strip()
            body = parts[i + 1].strip() if i + 1 < len(parts) else ''
            if body:
                chapters.append((title, body))
    if not chapters:
        chapters = [('Книга', text.strip())]
    return chapters


@login_required
def book_add(request):
    if not _is_author(request.user):
        return redirect('book_list')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        txt_form = TxtUploadForm(request.POST, request.FILES)
        file_given = bool(request.FILES.get('txt_file'))
        if form.is_valid() and (not file_given or txt_form.is_valid()):
            book = form.save(commit=False)
            book.author = request.user
            book.save()

            if file_given:
                _load_txt(book, txt_form.cleaned_data['txt_file'])
            return redirect('book_edit', book_id=book.id)
    else:
        form = BookForm()
        txt_form = TxtUploadForm()

    return render(request, 'book/book_form.html', {
        'form': form,
        'txt_form': txt_form,
        'title': 'Добавить книгу',
    })


def _load_txt(book, txt_file):
    raw = txt_file.read()
    text = _file_to_text(txt_file.name, raw)
    for i, (title, body) in enumerate(_split_txt_to_chapters(text), start=1):
        chapter = Chapter.objects.create(book=book, title=title, number=i, text=body)
        _notify_subscribers(book, chapter)


def _file_to_text(filename, raw):
    """txt -> utf-8, docx -> вытащить абзацы из word/document.xml (без библиотек)."""
    if filename.lower().endswith('.docx'):
        return _docx_to_text(raw)
    return raw.decode('utf-8', errors='replace')


def _docx_to_text(raw):
    import io
    import zipfile
    import xml.etree.ElementTree as ET

    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        xml = zf.read('word/document.xml')
    root = ET.fromstring(xml)
    ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    paragraphs = []
    for p in root.iter(ns + 'p'):
        line = ''.join(t.text or '' for t in p.iter(ns + 't'))
        paragraphs.append(line)
    return '\n'.join(paragraphs)


def _notify_subscribers(book, chapter):
    """Сообщение тем, у кого книга в закладках (кроме автора)."""
    users = User.objects.filter(
        bookmark_lists__bookmarks__book=book
    ).exclude(id=book.author_id).distinct()
    text = 'Вышла новая глава «%(title)s» в книге «%(book)s»'
    Notification.objects.bulk_create(
        [Notification(user=u, book=book, chapter=chapter, text=text)
         for u in users]
    )


@login_required
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id, author=request.user)
    chapters = book.chapters.all()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        txt_form = TxtUploadForm(request.POST, request.FILES)
        file_given = bool(request.FILES.get('txt_file'))
        if form.is_valid() and (not file_given or txt_form.is_valid()):
            form.save()
            if file_given:
                _load_txt(book, txt_form.cleaned_data['txt_file'])
            return redirect('book_edit', book_id=book.id)
    else:
        form = BookForm(instance=book)
        txt_form = TxtUploadForm()

    chapter_form = ChapterForm()
    return render(request, 'book/book_form.html', {
        'form': form,
        'txt_form': txt_form,
        'chapter_form': chapter_form,
        'book': book,
        'chapters': chapters,
        'title': f'Редактировать: {book.title}',
    })


@login_required
def chapter_add(request, book_id):
    book = get_object_or_404(Book, id=book_id, author=request.user)
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.book = book
            last = book.chapters.order_by('-number').first()
            chapter.number = (last.number + 1) if last else 1
            chapter.save()
            _notify_subscribers(book, chapter)
    return redirect('book_edit', book_id=book.id)


@login_required
def chapter_delete(request, book_id, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id, book__author=request.user)
    if request.method == 'POST':
        chapter.delete()
    return redirect('book_edit', book_id=chapter.book_id)


@login_required
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id, author=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('author_books')
    return render(request, 'book/book_delete.html', {'book': book})





@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    stats = {
        'books': request.user.books.count(),
        'comments': request.user.comments.count(),
        'ratings': request.user.ratings.count(),
        'bookmarks': Bookmark.objects.filter(list__user=request.user).count(),
        'lists': BookmarkList.objects.filter(user=request.user).count(),
    }
    my_books = request.user.books.all() if profile_obj.is_author else None
    return render(request, 'book/profile.html', {
        'profile_obj': profile_obj,
        'stats': stats,
        'my_books': my_books,
    })






def _ensure_default_lists(user):
    for name in ('Читаю', 'Прочитано'):
        BookmarkList.objects.get_or_create(user=user, name=name)


@login_required
def bookmarks(request):
    _ensure_default_lists(request.user)
    if request.method == 'POST':
        form = BookmarkListForm(request.POST)
        if form.is_valid():
            bl = form.save(commit=False)
            bl.user = request.user
            try:
                bl.save()
            except Exception:
                messages.error(request, tr(request, 'Такой список уже есть'))
            return redirect('bookmarks')
    else:
        form = BookmarkListForm()
        form.fields['name'].widget.attrs['placeholder'] = tr(request, 'Например: Любимое')

    lists = BookmarkList.objects.filter(user=request.user).prefetch_related('bookmarks__book')
    return render(request, 'book/bookmarks.html', {'lists': lists, 'form': form})


@login_required
def bookmark_list_delete(request, list_id):
    bl = get_object_or_404(BookmarkList, id=list_id, user=request.user)
    if request.method == 'POST':
        bl.delete()
        messages.success(request, tr(request, 'Список «%(name)s» удалён', name=bl.name))
    return redirect('bookmarks')


@login_required
def bookmark_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        _ensure_default_lists(request.user)
        list_id = request.POST.get('list_id')
        bl = BookmarkList.objects.filter(id=list_id, user=request.user).first()
        if bl:
            _, created = Bookmark.objects.get_or_create(list=bl, book=book)
            if created:
                messages.success(request, tr(request, 'Добавлено в «%(name)s»', name=bl.name))
    return redirect('book_detail', book_id=book_id)


@login_required
def bookmark_remove(request, bookmark_id):
    bm = get_object_or_404(Bookmark, id=bookmark_id, list__user=request.user)
    next_url = request.POST.get('next', '/bookmarks/')
    if not next_url.startswith('/'):
        next_url = '/bookmarks/'
    if request.method == 'POST':
        bm.delete()
        messages.success(request, tr(request, 'Убрано из закладок'))
    return redirect(next_url)








@login_required
def notifications(request):
    items = request.user.notifications.all()
    if request.method == 'POST':
        items.filter(is_read=False).update(is_read=True)
        return redirect('notifications')
    unread = items.filter(is_read=False).count()
    return render(request, 'book/notifications.html', {
        'items': items,
        'unread': unread,
    })
