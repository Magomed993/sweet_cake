from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class CakeLevel(models.Model):
    """Модель для хранения количества уровней торта"""

    amount = models.PositiveSmallIntegerField(unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.amount} уровень(я) (+{self.price}р)"


class CakeForm(models.Model):
    """Модель для хранения формы торта"""

    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} (+{self.price}р)"


class Topping(models.Model):
    """Модель для хранения топпинга"""

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} (+{self.price}р)"


class Berry(models.Model):
    """Модель для хранения ягод"""

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} (+{self.price}р)"


class Decor(models.Model):
    """Дополнительный декор, можно не добавлять."""

    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} (+{self.price}р)"


class Cake(models.Model):
    """Основная модель торта"""

    layers = models.ForeignKey(CakeLevel, on_delete=models.DO_NOTHING)
    shape = models.ForeignKey(CakeForm, on_delete=models.DO_NOTHING)
    topping = models.ForeignKey(Topping, on_delete=models.DO_NOTHING)
    berries = models.ForeignKey(Berry, on_delete=models.SET_NULL, blank=True, null=True)
    decor = models.ForeignKey(Decor, on_delete=models.SET_NULL, blank=True, null=True)
    inscription = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Торт ({self.shape.name}, {self.layers.amount})"


class Client(models.Model):
    """Клиент"""
    customer_name = models.CharField(verbose_name='имя', max_length=20)
    phone_number = PhoneNumberField(verbose_name='телефон', blank=True)
    email = models.EmailField(verbose_name='почта')

    def __str__(self):
        return self.customer_name


class Order(models.Model):
    """Модель для заказа"""
    cake = models.ForeignKey(Cake, verbose_name='торт', on_delete=models.PROTECT)
    client = models.ForeignKey(Client, verbose_name='клиент', on_delete=models.CASCADE, related_name='orders')
    address = models.TextField(verbose_name='адрес')
    desired_date = models.DateTimeField(verbose_name='дата')
    desired_time = models.TimeField(verbose_name='время')
    deliver_comment = models.TextField(max_length=200, verbose_name='комментарии', blank=True, null=True)
    total_cost = models.FloatField(verbose_name='общая стоимость', default=0.0)
    created_at = models.DateTimeField(verbose_name='дата создания заказа', default=timezone.now())

    def __str__(self):
        return f'{self.pk} - {self.client.name}'
