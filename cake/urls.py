from django.urls import path

from cake import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="main_page"),
    path("account/<int:user_id>/", views.account, name="account"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("register_order/", views.register_order, name="register_order"),
]
