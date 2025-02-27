from django.contrib.auth.models import User
from rest_framework.serializers import (
    CharField,
    EmailField,
    IntegerField,
    ModelSerializer,
    ValidationError,
)

from .models import Berry, Cake, CakeForm, CakeLevel, Client, Decor, Order, Topping


class CakeSerializer(ModelSerializer):
    """Сериализатор для модели торта"""

    layers = IntegerField(write_only=True)
    shape = CharField(write_only=True)
    topping = CharField(write_only=True)
    berries = CharField(write_only=True, required=False, allow_null=True)
    decor = CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Cake
        fields = ["layers", "shape", "topping", "berries", "decor", "inscription"]

    def create(self, validated_data):
        """Создаём Cake, находя ингредиенты по названиям"""

        try:
            layers = CakeLevel.objects.get(amount=validated_data.pop("layers"))
            shape = CakeForm.objects.get(name=validated_data.pop("shape"))
            topping = Topping.objects.get(name=validated_data.pop("topping"))

            berries_name = validated_data.pop("berries")
            berries = (
                None if berries_name == "нет" else Berry.objects.get(name=berries_name)
            )
            decor_name = validated_data.pop("decor")
            decor = None if decor_name == "нет" else Decor.objects.get(name=decor_name)

        except (
            CakeLevel.DoesNotExist,
            CakeForm.DoesNotExist,
            Topping.DoesNotExist,
            Berry.DoesNotExist,
            Decor.DoesNotExist,
        ) as e:
            raise ValidationError(f"Ошибка: {e}")

        cake, _ = Cake.objects.get_or_create(
            layers=layers,
            shape=shape,
            topping=topping,
            berries=berries,
            decor=decor,
            inscription=validated_data.get("inscription", ""),
        )

        return cake


class OrderSerializer(ModelSerializer):
    """Сериализатор для модели заказа"""

    cake = CakeSerializer()
    customer_name = CharField(write_only=True)
    phone_number = CharField(write_only=True)
    email = EmailField(write_only=True)

    class Meta:
        model = Order
        fields = [
            "cake",
            "customer_name",
            "phone_number",
            "email",
            "address",
            "desired_date",
            "desired_time",
            "comment",
            "deliver_comment",
            "total_cost",
        ]

    def create(self, validated_data):
        """Создание заказа с клиентом"""

        cake = CakeSerializer().create(validated_data.pop("cake"))

        phone_number = validated_data.pop("phone_number")
        user, _ = User.objects.get_or_create(
            username=phone_number, defaults={"is_active": True}
        )
        client, _ = Client.objects.get_or_create(
            user=user,
            defaults={
                "customer_name": validated_data.pop("customer_name"),
                "email": validated_data.pop("email"),
                "phone_number": phone_number,
            },
        )

        return Order.objects.create(client=client, cake=cake, **validated_data)
