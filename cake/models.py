from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import inform_tg_bot as tg_bot



class CakeLevel(models.Model):
    """Модель для хранения количества уровней торта"""

    amount = models.PositiveSmallIntegerField(unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.amount} уровень(я)"


class CakeForm(models.Model):
    """Модель для хранения формы торта"""

    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Topping(models.Model):
    """Модель для хранения топпинга"""

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Berry(models.Model):
    """Модель для хранения ягод"""

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Decor(models.Model):
    """Дополнительный декор, можно не добавлять."""

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Cake(models.Model):
    """Основная модель торта"""

    layers = models.ForeignKey(CakeLevel, on_delete=models.DO_NOTHING)
    shape = models.ForeignKey(CakeForm, on_delete=models.DO_NOTHING)
    topping = models.ForeignKey(Topping, on_delete=models.DO_NOTHING)
    berries = models.ForeignKey(Berry, on_delete=models.SET_NULL, blank=True, null=True)
    decor = models.ForeignKey(Decor, on_delete=models.SET_NULL, blank=True, null=True)
    inscription = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Торт ({self.layers.amount} уровень(я), {self.shape.name})"


class Client(models.Model):
    """Модель клиента, связанная с пользователем Django"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    customer_name = models.CharField(verbose_name="имя", max_length=20)
    phone_number = PhoneNumberField(verbose_name="телефон", blank=True)
    email = models.EmailField(verbose_name="почта")

    def __str__(self):
        return self.customer_name

    def model_to_dict(self):
        """
        Преобразует объект Client в словарь.
        """

        return {
            "id": self.pk,
            "customer_name": self.customer_name,
            "phone_number": str(self.phone_number) if self.phone_number else None,
            "email": self.email,
        }


class Order(models.Model):
    """Модель для заказа"""

    cake = models.ForeignKey(Cake, verbose_name="торт", on_delete=models.PROTECT)
    client = models.ForeignKey(
        Client, verbose_name="клиент", on_delete=models.CASCADE, related_name="orders"
    )
    address = models.TextField(verbose_name="адрес")
    desired_date = models.DateTimeField(verbose_name="дата")
    desired_time = models.TimeField(verbose_name="время")
    comment = models.TextField(
        max_length=200, verbose_name="комментарии к торту", blank=True, null=True
    )
    deliver_comment = models.TextField(
        max_length=200, verbose_name="комментарии курьеру", blank=True, null=True
    )
    total_cost = models.FloatField(verbose_name="общая стоимость", default=0.0)
    created_at = models.DateTimeField(
        verbose_name="дата создания заказа", default=timezone.now
    )

    def __str__(self):
        return f"{self.pk} - {self.client.customer_name}"


@receiver(post_save, sender=Order)
def order_post_save(instance, created, **kwargs):
    created_message = tg_bot.make_order_details(instance, created)
    tg_bot.send_note(created_message)
    return
