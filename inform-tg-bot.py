import telebot
from environs import Env

def make_message():
    message=f''
    return message

def send_note(message='Default_message'):
    env = Env()
    env.read_env()

    TG_BOT_TOKEN = env.str('TG_BOT_TOKEN')
    TG_USER_ID = env.str('TG_USER_ID')

    bot = telebot.TeleBot(TG_BOT_TOKEN)
    bot.send_message(TG_USER_ID, message)
    return

send_note()