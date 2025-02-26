import json

from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cake.models import Berry, CakeForm, CakeLevel, Decor, Topping

User = get_user_model()


class IndexView(View):
    def setup(self, request, *args, **kwargs):
        models = {
            "Levels": CakeLevel.objects.all(),
            "Forms": CakeForm.objects.all(),
            "Toppings": Topping.objects.all(),
            "Berries": Berry.objects.all(),
            "Decors": Decor.objects.all(),
        }
        self.context = {"DATA": {}, "Costs": {"Words": 500}}

        for key, queryset in models.items():
            items = list(queryset)
            self.context["DATA"][key] = [
                "не выбрано" if key not in ("Berries", "Decors") else "нет"
            ] + [obj.name if hasattr(obj, "name") else obj.amount for obj in items]
            self.context["Costs"][key] = [0] + [int(obj.price) for obj in items]

        super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(request, "index.html", self.context)
    

@transaction.atomic
@api_view(["POST"])
def register_order(request: HttpRequest):

    # TODO: добавить serializer = OrderSerializer(data=request.data)
    print(request.data)
    # {
    #     "cake": {
    #         "level": 2,
    #         "form": "Квадрат",
    #         "topping": "Клубничный сироп",
    #         "berry": "Малина",
    #         "decoration": "Фундук",
    #         "title": "С днем рождения",
    #     },
    #     "comment": "Хочу мнооого малины",
    #     "customer_name": "Иван",
    #     "phone_number": "89999601221",
    #     "email": "mail@mail.ru",
    #     "address": "Москва, ул. Пушкина, дом Колотушкина",
    #     "desired_date": "2025-03-01",
    #     "desired_time": "10:00",
    #     "deliver_comment": "Домофон не работает",
    #     "total_сost": 2800,
    # }
    return Response({"message": "success"})


def account(request: HttpRequest, user_id: int) -> HttpResponse:
    """Обрабатывает страницу личного кабинета пользователя."""
    
    if request.user.id != user_id:
        return HttpResponse("Доступ запрещен", status=403)

    # TODO: Брать заказы из БД и передать в context

    return render(request, "lk.html")


class UserLoginView(LoginView):
    """Авторизация на сайте"""

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        phone = data.get("phone")
        if not phone:
            return JsonResponse({"error": "Номер телефона не указан"}, status=400)

        user, created = User.objects.get_or_create(
            username=phone, defaults={"is_active": True}
        )
        login(request, user)

        return JsonResponse({"message": "Успешная авторизация", "user_id": user.pk})


class UserLogoutView(LogoutView):
    """Выход с сайта"""

    next_page = reverse_lazy("main_page")
