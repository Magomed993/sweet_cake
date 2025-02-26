from django.db import models


class CakeLayer(models.Model):
    """Модель для хранения количества уровней торта"""

    amount = models.PositiveSmallIntegerField(unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.amount} уровень(я) (+{self.price}р)"


class CakeShape(models.Model):
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

    layers = models.ForeignKey(CakeLayer, on_delete=models.DO_NOTHING)
    shape = models.ForeignKey(CakeShape, on_delete=models.DO_NOTHING)
    topping = models.ForeignKey(Topping, on_delete=models.DO_NOTHING)
    berries = models.ForeignKey(Berry, on_delete=models.SET_NULL, blank=True, null=True)
    decor = models.ForeignKey(Decor, on_delete=models.SET_NULL, blank=True, null=True)
    inscription = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Торт ({self.shape.name}, {self.layers.amount})"
