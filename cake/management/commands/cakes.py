from django.core.management.base import BaseCommand
from django.apps import apps

DATA = [
    {"model": "cake.CakeLayer", "pk": 1, "fields": {"amount": 1, "price": 400}},
    {"model": "cake.CakeLayer", "pk": 2, "fields": {"amount": 2, "price": 750}},
    {"model": "cake.CakeLayer", "pk": 3, "fields": {"amount": 3, "price": 1100}},
    {"model": "cake.CakeShape", "pk": 1, "fields": {"name": "Квадрат", "price": 600}},
    {"model": "cake.CakeShape", "pk": 2, "fields": {"name": "Круг", "price": 400}},
    {"model": "cake.CakeShape", "pk": 3, "fields": {"name": "Прямоугольник", "price": 1000}},
    {"model": "cake.Topping", "pk": 1, "fields": {"name": "Без", "price": 0}},
    {"model": "cake.Topping", "pk": 2, "fields": {"name": "Белый соус", "price": 200}},
    {"model": "cake.Topping", "pk": 3, "fields": {"name": "Карамельный сироп", "price": 180}},
    {"model": "cake.Topping", "pk": 4, "fields": {"name": "Кленовый сироп", "price": 200}},
    {"model": "cake.Topping", "pk": 5, "fields": {"name": "Клубничный сироп", "price": 300}},
    {"model": "cake.Topping", "pk": 6, "fields": {"name": "Черничный сироп", "price": 350}},
    {"model": "cake.Topping", "pk": 7, "fields": {"name": "Молочный шоколад", "price": 200}},
    {"model": "cake.Berry", "pk": 1, "fields": {"name": "Малина", "price": 300}},
    {"model": "cake.Berry", "pk": 2, "fields": {"name": "Клубника", "price": 500}},
    {"model": "cake.Berry", "pk": 3, "fields": {"name": "Ежевика", "price": 400}},
    {"model": "cake.Berry", "pk": 4, "fields": {"name": "Голубика", "price": 450}},
    {"model": "cake.Decor", "pk": 1, "fields": {"name": "Фисташки", "price": 300}},
    {"model": "cake.Decor", "pk": 2, "fields": {"name": "Безе", "price": 400}},
    {"model": "cake.Decor", "pk": 3, "fields": {"name": "Фундук", "price": 350}},
    {"model": "cake.Decor", "pk": 4, "fields": {"name": "Пекан", "price": 300}},
    {"model": "cake.Decor", "pk": 5, "fields": {"name": "Маршмеллоу", "price": 200}},
    {"model": "cake.Decor", "pk": 6, "fields": {"name": "Марципан", "price": 280}},
]

class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными для тортов."

    def handle(self, *args, **kwargs):
        for entry in DATA:
            app_label, model_name = entry["model"].split(".")
            model = apps.get_model(app_label, model_name)
            
            obj, created = model.objects.update_or_create(
                pk=entry["pk"], defaults=entry["fields"]
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлен: {obj}"))
            else:
                self.stdout.write(self.style.WARNING(f"Обновлен: {obj}"))

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена тестовыми данными! 🎂"))
