import logging
from django.db import models
import click_counter.services as services

logger = logging.getLogger(__name__)

class ShortLink(models.Model):
    
    PLATFORMS = [
        ('vk', 'vk_cc.ru'),
    ]

    original_url = models.URLField(max_length=255, blank=True, null=True, verbose_name='Оригинальная ссылка') # Оригинальная ссылка
    shortener = models.CharField(max_length=255, blank=True, null=True, choices=PLATFORMS, verbose_name='Сервис сокращения ссылок')  # Платформа для сокращения ссылок
    short_url = models.URLField(max_length=255, unique=True, blank=True, null=True, db_index=True, verbose_name='Короткая ссылка')  # Короткая ссылка
    clicks_count = models.PositiveIntegerField(default=0, verbose_name='Количество переходов по ссылке')  # Количество переходов по ссылке
    notes = models.CharField(max_length=255, blank=True, verbose_name='Примечания') # Примечания

    def __str__(self):
        return f"Оригинальная ссылка: {self.original_url}\nКороткая ссылка: {self.short_url} - Количество переходов: {self.clicks_count})"
    
    
    def save(self, *args, **kwargs):
        shorteners = {
        'vk': services.shorten_link_vk,
        }
        if not self.short_url and self.shortener in shorteners:
            try:
                shortener = shorteners[self.shortener]
                self.short_url = shortener(self.original_url)
            except Exception as err:
                logger.error("Не получилось сократить ссылку: %s", err, exc_info=True)
                self.short_url = None
        super().save(*args, **kwargs)
    
    
    def update_clicks(self):
        try:
            clicks_count = services.count_clicks(self.short_url)
            self.clicks_count = clicks_count
            super().save(update_fields=['clicks_count'])
        except Exception as err:
            logger.error("Невозможно подсчитать ссылки: %s", err, exc_info=True)
        return
