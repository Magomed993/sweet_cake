from django.db import models
from click_counter.services import count_clicks


class ShortLink(models.Model):
    short_url = models.URLField(max_length=255, unique=True, db_index=True)  # Короткая ссылка
    ad_platform = models.CharField(max_length=255, blank=True)  # Платформа
    clicks_count = models.PositiveIntegerField(default=0)  # Количество переходов по ссылке

    def __str__(self):
        return f"Платформа: {self.ad_platform}\nСсылка: {self.short_url} - Количество переходов: {self.clicks_count})"
    
    def update_clicks(self):
        clicks_count = count_clicks(self.short_url)
        self.clicks_count = clicks_count
        self.save()
        return
