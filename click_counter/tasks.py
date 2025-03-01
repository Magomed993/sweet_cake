from click_counter.models import ShortLink
from background_task import background


@background(schedule=86400)  # Будет запускаться раз в сутки (86400 секунд)
def update_click_counts():
    links_to_update = []
    for link in ShortLink.objects.all():
        link.update_clicks()
        links_to_update.append(link)
    ShortLink.objects.bulk_update(links_to_update, ['clicks_count'])
