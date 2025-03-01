from django.contrib import admin
from click_counter.models import ShortLink
from click_counter.services import count_clicks

# Register your models here.


def reset_values(modeladmin, request, queryset):
    queryset.update(
        clicks_count=0,
    )
    modeladmin.message_user(request, "Значения успешно обнулены!")


reset_values.short_description = "Обнулить значения"


def update_clicks_once(modeladmin, request, queryset):
    links_to_update = []
    for link in queryset:
        link.update_clicks()
        links_to_update.append(link)
    ShortLink.objects.bulk_update(links_to_update, ['clicks_count'])
    modeladmin.message_user(request, "Данные обновлены")


update_clicks_once.short_description = "Обновить данные"


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ("short_url", "ad_platform", "clicks_count")
    search_fields = ("short_url", "ad_platform")
    actions = [reset_values, update_clicks_once]
