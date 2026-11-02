from django.apps import AppConfig


class BookConfig(AppConfig):
    name = 'book'

    def ready(self):
        from django.db.models.signals import post_save
        from django.dispatch import receiver
        from django.contrib.auth.models import User

        @receiver(post_save, sender=User)
        def create_profile(sender, instance, created, **kwargs):
            if created:
                from .models import Profile, BookmarkList
                Profile.objects.get_or_create(user=instance)
                for name in ('Читаю', 'Прочитано'):
                    BookmarkList.objects.get_or_create(user=instance, name=name)
