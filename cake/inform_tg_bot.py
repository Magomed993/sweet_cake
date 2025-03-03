import telebot
from environs import Env
from datetime import datetime
from textwrap import dedent


def make_order_details(instance={}, created: bool = True) -> str:
    """Создает текст с информацией о заказе по шаблону"""

    order_type = "Создан"
    if not created:
        order_type = "Изменен"

    order_date = instance.created_at.strftime("%d-%m-%Y")

    order_details = dedent(f"""
    {order_type} заказ №{instance.id} от {order_date}:
    количество уровней - {instance.cake.layers},
    форма - {instance.cake.shape},
    топпинг - {instance.cake.topping}
    _______________
    Заказчик: {instance.client.customer_name}""")

    if instance.client.phone_number:
        order_details += f"\nНомер телефона: {instance.client.phone_number}"
        
    des_date = instance.desired_date.strftime("%d-%m-%Y")
    des_time = instance.desired_time.strftime("%H:%M")
    cost = f"{int(instance.total_cost)} руб."

    order_details += dedent(f"""
    Адрес доставки: {instance.address}
    Дата и время доставки: {des_date} в {des_time}
    _______________
    Итоговая стоимость: {cost}""")

    return order_details


def send_note(message: str = "Default_message") -> None:
    env = Env()
    env.read_env()
    tg_bot_token = env.str("TG_BOT_TOKEN")
    tg_user_id = env.str("TG_USER_ID")

    bot = telebot.TeleBot(tg_bot_token)
    bot.send_message(tg_user_id, message)
    return
