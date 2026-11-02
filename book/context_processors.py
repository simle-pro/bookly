def unread_notifications(request):
    """Счётчик непрочитанных сообщений для шапки."""
    if request.user.is_authenticated:
        return {'unread_count': request.user.notifications.filter(is_read=False).count()}
    return {'unread_count': 0}


def current_lang(request):
    """Текущий язык для шаблонов."""
    from .translations import get_lang, LANGS
    return {
        'LANG': get_lang(request),
        'LANGS': LANGS,
    }
