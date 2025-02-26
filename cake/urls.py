from django.urls import path

from cake import views

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("account", views.account, name="account"),
]
