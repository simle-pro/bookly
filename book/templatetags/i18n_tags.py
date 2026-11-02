from django import template

from ..translations import translate, get_lang

register = template.Library()


@register.simple_tag(takes_context=True)
def tr(context, text, **kwargs):
    """Перевод строки: {% tr 'Сообщения' %} или {% tr 'Привет, %(name)s' name=user %}."""
    request = context.get('request')
    lang = get_lang(request) if request else 'ru'
    return translate(lang, text, **kwargs)


@register.simple_tag(takes_context=True)
def tr_notify(context, item):
    """Перевод текста уведомления с подстановкой названий главы и книги."""
    request = context.get('request')
    lang = get_lang(request) if request else 'ru'
    return translate(lang, item.text,
                     title=item.chapter.title if item.chapter_id else '',
                     book=item.book.title)
