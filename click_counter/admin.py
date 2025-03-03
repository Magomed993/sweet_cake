from django.contrib import admin
from click_counter.models import ShortLink

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
    list_display = ["original_url", "shortener", "short_url", "clicks_count", "notes"]
    search_fields = ("original_url", "shortener", "short_url")
    actions = [reset_values, update_clicks_once]
    readonly_fields = ["clicks_count"]