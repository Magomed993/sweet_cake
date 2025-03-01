from django.apps import AppConfig


class ClickCounterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "click_counter"

    def ready(self):
        from click_counter.tasks import update_click_counts
        update_click_counts()
