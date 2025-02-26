from django.contrib import admin

from .models import CakeLevel, CakeForm, Topping, Berry, Decor, Cake
from .models import Order, Client


class ClientOrderInline(admin.TabularInline):
    model = Order
    fields = ['id', 'created_at', 'desired_date', 'desired_time', 'total_cost']
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [
        ClientOrderInline
    ]
    list_display = ['customer_name', 'phone_number', 'email']


@admin.register(CakeLevel)
class CakeLavelAdmin(admin.ModelAdmin):
    list_display = ['amount', 'price']


@admin.register(CakeForm)
class CakeFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Decor)
class DecorAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ['layers', 'shape', 'topping', 'berries', 'decor']

