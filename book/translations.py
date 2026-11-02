"""Переводы сайта: словари без gettext (ключи — русские строки)."""

LANGS = [
    ('ru', '🇷🇺 Русский'),
    ('en', '🇬🇧 English'),
    ('de', '🇩🇪 Deutsch'),
]

# Язык -> {русская строка: перевод}
TRANSLATIONS = {
    'en': {
        # Шапка / общее
        'КнигоСайт': 'BookSite',
        'КнигоСайт — читай и слушай книги онлайн': 'BookSite — read and listen to books online',
        'Поиск книги или автора…  (Ctrl+K)': 'Search book or author…  (Ctrl+K)',
        'Найти': 'Search',
        'Язык': 'Language',
        'Сменить тему': 'Switch theme',
        'Сообщения': 'Messages',
        'Закладки': 'Bookmarks',
        'Мои книги': 'My books',
        'Выйти': 'Log out',
        'Вход': 'Sign in',
        'Регистрация': 'Sign up',

        # Главная
        'Все книги': 'All books',
        'Результаты поиска по запросу': 'Search results for',
        'Нет оценок': 'No ratings',
        'Книг пока нет.': 'No books yet.',

        # Страница книги
        'Автор': 'Author',
        'оценок': 'ratings',
        'Пока нет оценок': 'No ratings yet',
        'Читать': 'Read',
        'Слушать': 'Listen',
        'В закладки': 'To bookmarks',
        'Добавить': 'Add',
        'в': 'in',
        'Ваша оценка': 'Your rating',
        'Поставить оценку': 'Rate this book',
        'Оценить': 'Rate',
        'Комментарии': 'Comments',
        'Войдите': 'Sign in',
        'чтобы оставить комментарий.': 'to leave a comment.',
        'Комментариев пока нет.': 'No comments yet.',
        'Отправить': 'Send',

        # Читалка
        'Чтение': 'Reading',
        'По главам': 'By chapters',
        'Сплошной': 'Continuous',
        'В этой книге пока нет глав.': 'This book has no chapters yet.',
        'Содержание': 'Contents',
        'Главы': 'Chapters',
        'Пред.': 'Prev',
        'След.': 'Next',

        # Плеер
        'Аудиокнига': 'Audiobook',
        'Ваш браузер не поддерживает аудио.': 'Your browser does not support audio.',
        'Назад к книге': 'Back to book',

        # Кабинет автора
        'Название': 'Title',
        'Жанр': 'Genre',
        'Глав': 'Ch.',
        'Аудио': 'Audio',
        'Ред.': 'Edit',
        'Удал.': 'Del.',
        'Вы ещё не добавили книг.': 'You have not added any books yet.',
        'Добавить книгу': 'Add book',

        # Форма книги
        'Описание': 'Description',
        'Обложка': 'Cover',
        'Аудио (mp3)': 'Audio (mp3)',
        'Файл .txt или .docx (разбивается на главы)': 'File .txt or .docx (split into chapters)',
        'Главы ищутся по строкам «Глава 1», «Глава 2»… или «# …». Форматы: .txt и .docx':
            'Chapters are found by lines “Chapter 1”, “Chapter 2”… or “# …”. Formats: .txt and .docx',
        'Сохранить': 'Save',
        'Назад': 'Back',
        'Добавить главу': 'Add chapter',
        'Удалить главу': 'Delete chapter',
        'удалить': 'delete',
        'Глав пока нет — загрузите txt или добавьте вручную.':
            'No chapters yet — upload a txt or add one manually.',

        # Удаление книги
        'Удалить книгу': 'Delete book',
        'Удалить книгу?': 'Delete this book?',
        'и все её главы, оценки и комментарии будут удалены безвозвратно.':
            'and all its chapters, ratings and comments will be deleted forever.',
        'безвозвратно?': 'forever?',
        'Да, удалить': 'Yes, delete',
        'Отмена': 'Cancel',

        # Профиль
        'Профиль': 'Profile',
        'Автор': 'Author',
        'Читатель': 'Reader',
        'с': 'since',
        'закладок': 'bookmarks',
        'списков': 'lists',
        'комментариев': 'comments',
        'книг': 'books',
        'Мои закладки': 'My bookmarks',
        'Мои комментарии': 'My comments',

        # Закладки
        'Новый список': 'New list',
        'Создать': 'Create',
        'Удалить список': 'Delete list',
        'удалить список': 'delete list',
        'Пусто. Добавляйте книги со страницы книги.':
            'Empty. Add books from the book page.',
        'убрать': 'remove',

        # Сообщения
        'Отметить всё прочитанным': 'Mark all as read',
        'Непрочитанных': 'Unread',
        'Сообщений пока нет. Добавьте книгу в закладки — и вам придёт уведомление о новых главах.':
            'No messages yet. Add a book to your bookmarks — you will get notified about new chapters.',

        # Регистрация / вход
        'Я регистрируюсь как': 'I am signing up as',
        'Логин': 'Username',
        'Пароль': 'Password',
        'Повторите пароль': 'Repeat password',
        'Зарегистрироваться': 'Sign up',
        'Уже есть аккаунта?': 'Already have an account?',
        'Уже есть аккаунт?': 'Already have an account?',
        'Войти': 'Sign in',
        'Нет аккаунта?': "Don't have an account?",

        # Сообщения (flash)
        'Регистрация прошла успешно!': 'Registration successful!',
        'Неверный логин или пароль': 'Invalid username or password',
        'Это кабинет только для авторов': 'This area is for authors only',
        'Такой список уже есть': 'This list already exists',
        'Убрано из закладок': 'Removed from bookmarks',
        'Вышла новая глава «%(title)s» в книге «%(book)s»':
            'New chapter “%(title)s” released in “%(book)s”',
        'Список «%(name)s» удалён': 'List “%(name)s” deleted',
        'Добавлено в «%(name)s»': 'Added to “%(name)s”',

        # Формы: ошибки и подсказки
        'Нужен файл .txt или .docx': 'A .txt or .docx file is required',
        'Файл больше 5 МБ': 'File is larger than 5 MB',
        'Похоже, это не документ Word': 'This does not look like a Word document',
        'Файл повреждён или не .docx': 'File is corrupted or not a .docx',
        'Ваш комментарий...': 'Your comment...',
        'Например: Любимое': 'e.g. Favorites',
    },
    'de': {
        # Шапка / общее
        'КнигоСайт': 'BuchSeite',
        'КнигоСайт — читай и слушай книги онлайн': 'BuchSeite — Bücher lesen und hören',
        'Поиск книги или автора…  (Ctrl+K)': 'Buch oder Autor suchen…  (Ctrl+K)',
        'Найти': 'Suchen',
        'Язык': 'Sprache',
        'Сменить тему': 'Design wechseln',
        'Сообщения': 'Nachrichten',
        'Закладки': 'Lesezeichen',
        'Мои книги': 'Meine Bücher',
        'Выйти': 'Abmelden',
        'Вход': 'Anmelden',
        'Регистрация': 'Registrieren',

        # Главная
        'Все книги': 'Alle Bücher',
        'Результаты поиска по запросу': 'Suchergebnisse für',
        'Нет оценок': 'Keine Bewertungen',
        'Книг пока нет.': 'Noch keine Bücher.',

        # Страница книги
        'Автор': 'Autor',
        'оценок': 'Bewertungen',
        'Пока нет оценок': 'Noch keine Bewertungen',
        'Читать': 'Lesen',
        'Слушать': 'Hören',
        'В закладки': 'Zu Lesezeichen',
        'Добавить': 'Hinzufügen',
        'в': 'in',
        'Ваша оценка': 'Ihre Bewertung',
        'Поставить оценку': 'Bewerten',
        'Оценить': 'Bewerten',
        'Комментарии': 'Kommentare',
        'Войдите': 'Anmelden',
        'чтобы оставить комментарий.': 'um einen Kommentar zu hinterlassen.',
        'Комментариев пока нет.': 'Noch keine Kommentare.',
        'Отправить': 'Senden',

        # Читалка
        'Чтение': 'Lesen',
        'По главам': 'Nach Kapiteln',
        'Сплошной': 'Durchgehend',
        'В этой книге пока нет глав.': 'Dieses Buch hat noch keine Kapitel.',
        'Содержание': 'Inhalt',
        'Главы': 'Kapitel',
        'Пред.': 'Zurück',
        'След.': 'Weiter',

        # Плеер
        'Аудиокнига': 'Hörbuch',
        'Ваш браузер не поддерживает аудио.': 'Ihr Browser unterstützt kein Audio.',
        'Назад к книге': 'Zurück zum Buch',

        # Кабинет автора
        'Название': 'Titel',
        'Жанр': 'Genre',
        'Глав': 'Kap.',
        'Аудио': 'Audio',
        'Ред.': 'Bearb.',
        'Удал.': 'Lösch.',
        'Вы ещё не добавили книг.': 'Sie haben noch keine Bücher hinzugefügt.',
        'Добавить книгу': 'Buch hinzufügen',

        # Форма книги
        'Описание': 'Beschreibung',
        'Обложка': 'Umschlag',
        'Аудио (mp3)': 'Audio (mp3)',
        'Файл .txt или .docx (разбивается на главы)': 'Datei .txt oder .docx (wird in Kapitel geteilt)',
        'Главы ищутся по строкам «Глава 1», «Глава 2»… или «# …». Форматы: .txt и .docx':
            'Kapitel werden anhand von „Kapitel 1“, „Kapitel 2“… oder „# …“ erkannt. Formate: .txt und .docx',
        'Сохранить': 'Speichern',
        'Назад': 'Zurück',
        'Добавить главу': 'Kapitel hinzufügen',
        'Удалить главу': 'Kapitel löschen',
        'удалить': 'löschen',
        'Глав пока нет — загрузите txt или добавьте вручную.':
            'Noch keine Kapitel — laden Sie eine txt hoch oder fügen Sie manuell hinzu.',

        # Удаление книги
        'Удалить книгу': 'Buch löschen',
        'Удалить книгу?': 'Dieses Buch löschen?',
        'и все её главы,оценки и комментарии будут удалены безвозвратно.':
            'und alle Kapitel, Bewertungen und Kommentare werden endgültig gelöscht.',
        'и все её главы, оценки и комментарии будут удалены безвозвратно.':
            'und alle Kapitel, Bewertungen und Kommentare werden endgültig gelöscht.',
        'безвозвратно?': 'endgültig?',
        'Да, удалить': 'Ja, löschen',
        'Отмена': 'Abbrechen',

        # Профиль
        'Профиль': 'Profil',
        'Читатель': 'Leser',
        'с': 'seit',
        'закладок': 'Lesezeichen',
        'списков': 'Listen',
        'комментариев': 'Kommentare',
        'книг': 'Bücher',
        'Мои закладки': 'Meine Lesezeichen',
        'Мои комментарии': 'Meine Kommentare',

        # Закладки
        'Новый список': 'Neue Liste',
        'Создать': 'Erstellen',
        'Удалить список': 'Liste löschen',
        'удалить список': 'Liste löschen',
        'Пусто. Добавляйте книги со страницы книги.': 'Leer. Fügen Sie Bücher von der Buchseite hinzu.',
        'убрать': 'entfernen',

        # Сообщения
        'Отметить всё прочитанным': 'Alle als gelesen markieren',
        'Непрочитанных': 'Ungelesen',
        'Сообщений пока нет. Добавьте книгу в закладки — и вам придёт уведомление о новых главах.':
            'Noch keine Nachrichten. Fügen Sie ein Buch zu Lesezeichen hinzu — Sie werden über neue Kapitel benachrichtigt.',

        # Регистрация / вход
        'Я регистрируюсь как': 'Ich registriere mich als',
        'Логин': 'Benutzername',
        'Пароль': 'Passwort',
        'Повторите пароль': 'Passwort wiederholen',
        'Зарегистрироваться': 'Registrieren',
        'Уже есть аккаунт?': 'Sie haben bereits ein Konto?',
        'Войти': 'Anmelden',
        'Нет аккаунта?': 'Noch kein Konto?',

        # Сообщения (flash)
        'Регистрация прошла успешно!': 'Registrierung erfolgreich!',
        'Неверный логин или пароль': 'Falscher Benutzername oder Passwort',
        'Это кабинет только для авторов': 'Dieser Bereich ist nur für Autoren',
        'Такой список уже есть': 'Diese Liste gibt es bereits',
        'Убрано из закладок': 'Aus Lesezeichen entfernt',
        'Вышла новая глава «%(title)s» в книге «%(book)s»':
            'Neues Kapitel „%(title)s“ erschienen in „%(book)s“',
        'Список «%(name)s» удалён': 'Liste „%(name)s“ gelöscht',
        'Добавлено в «%(name)s»': 'Hinzugefügt zu „%(name)s“',

        # Формы: ошибки и подсказки
        'Нужен файл .txt или .docx': 'Eine .txt- oder .docx-Datei erforderlich',
        'Файл больше 5 МБ': 'Datei ist größer als 5 MB',
        'Похоже, это не документ Word': 'Das sieht nicht nach einem Word-Dokument aus',
        'Файл повреждён или не .docx': 'Datei ist beschädigt oder keine .docx',
        'Ваш комментарий...': 'Ihr Kommentar...',
        'Например: Любимое': 'z. B. Favoriten',
    },
}


def translate(lang, text, **kwargs):
    """Вернуть перевод text на lang; ru — исходный текст."""
    result = TRANSLATIONS.get(lang, {}).get(text, text)
    if kwargs:
        try:
            result = result % kwargs
        except (KeyError, TypeError, ValueError):
            pass
    return result


def get_lang(request):
    """Язык из cookie, иначе ru."""
    lang = request.COOKIES.get('lang', 'ru')
    return lang if lang in TRANSLATIONS or lang == 'ru' else 'ru'
