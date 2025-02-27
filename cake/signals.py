from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Client


@receiver(post_save, sender=User)
def create_user_client(sender, instance, created, **kwargs):
    """Создаёт объект Client при создании нового пользователя."""
    if created:
        Client.objects.create(user=instance, phone_number=instance.username)


@receiver(post_save, sender=User)
def save_user_client(sender, instance, **kwargs):
    """Сохраняет объект Client при сохранении пользователя."""
    instance.client.save()
