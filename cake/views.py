import json

from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

User = get_user_model()


def main_page(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


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
