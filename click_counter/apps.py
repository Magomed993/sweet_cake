import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class ClickCounterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "click_counter"

    def ready(self):
        from django.db.utils import OperationalError, ProgrammingError

        from click_counter.tasks import update_click_counts

        try:
            update_click_counts()
        except (OperationalError, ProgrammingError) as e:
            logger.warning(f"Не удалось запустить update_click_counts: {e}")

