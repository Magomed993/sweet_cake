import requests
from urllib.parse import urlparse
from environs import Env


def get_netloc(short_url: str) -> str:
    """Определяет нетлок короткой ссылки"""
    if not short_url.startswith(("http://", "https://")):
        short_url = "https://" + short_url
    parsed_url = urlparse(short_url)
    return parsed_url.netloc


def notify_missing_method(short_url: str) -> int:
    """Уведомляет о невозможности подсчета переходов по ссылке"""
    netloc = get_netloc(short_url)
    print(f'Метод подсчета количества переходов по ссылке "{netloc}" отсутствует')
    return 0


def get_vk_clicks_count(short_url: str) -> int:
    """Получает количество переходов по короткой ссылке через VK API."""
    env = Env()
    env.read_env()
    vk_token = env.str("VK_SERVICE_TOKEN")
    link_key = urlparse(short_url).path[1:]
    parameters = {
        "access_token": vk_token,
        "v": "5.199",
        "key": link_key,
        "source": "vk_cc",
        "access_key": "",
        "interval": "forever",
        "intervals_count": 1,
        "extended": 0,
    }
    vk_clicks_count = 0
    try:
        response = requests.post(
            "https://api.vk.ru/method/utils.getLinkStats", data=parameters, timeout=20
        )
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("response", {}).get("stats"):
            vk_clicks_count = int(response_data["response"]["stats"][0]["views"])
        elif response_data.get("error"):
            print(f"Ошибка VK API: {response_data.get('error', {}).get('error_msg')}")
    except requests.RequestException as e:
        print(f"Ошибка при запросе к VK API: {e}")
    return vk_clicks_count


def count_clicks(short_url: str) -> int:
    """Получает число переходов по коротким ссылкам доступных сервисов"""
    netloc_handlers = {
        "vk.cc": get_vk_clicks_count,
    }
    netloc = get_netloc(short_url)
    handler = netloc_handlers.get(netloc, notify_missing_method)
    clicks_counted = 0
    if handler(short_url):
        clicks_counted = handler(short_url)
    return clicks_counted
