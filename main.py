import telebot
import datetime
import time
import threading
import random

# Токен бота
bot = telebot.TeleBot('TOKEN')

# Хранилище языковых настроек пользователей
user_language = {}

# Словарь с текстами на разных языках
texts = {
    'ru': {
        'welcome': 'Привет! Я чат бот, который будет напоминать тебе пить водичку!',
        'help': "Список команд:\n/start - Начать работу с ботом и получить напоминания о питье воды\n/fact - Получить интересный факт о воде\n/help - Получить информацию о командах бота\n/language - Сменить язык",
        'fact': 'Лови факт о воде:',
        'reminder': 'Напоминание - выпей стакан воды',
        'facts': [
            "Вода - единственное вещество на Земле, которое существует в трех различных состояниях: жидком, твердом и газообразном.",
            "Тело взрослого человека на 60% состоит из воды."
        ]
    },
    'en': {
        'welcome': 'Hello! I am a chat bot that will remind you to drink water!',
        'help': "List of commands:\n/start - Start working with the bot and receive reminders to drink water\n/fact - Get an interesting fact about water\n/help - Get information about the bot's commands\n/language - Change language",
        'fact': 'Here is a water fact:',
        'reminder': 'Reminder - drink a glass of water',
        'facts': [
            "Water is the only substance on Earth that exists in three different states: solid, liquid, and gas.",
            "An adult human body is about 60% water."
        ]
    }
}

# Обработчик команды start
@bot.message_handler(commands=['start'])
def start_message(message):
    user_language[message.chat.id] = 'ru'  # Задаем стандартный язык
    bot.reply_to(message, texts[user_language[message.chat.id]]['welcome'])
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

# Обработчик команды help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, texts[user_language[message.chat.id]]['help'])

# Обработчик команды fact
@bot.message_handler(commands=['fact'])
def fact_message(message):
    language = user_language[message.chat.id]
    random_fact = random.choice(texts[language]['facts'])
    bot.reply_to(message, f'{texts[language]["fact"]} {random_fact}')

# Обработчик команды language
@bot.message_handler(commands=['language'])
def change_language(message):
    if user_language[message.chat.id] == 'ru':
        user_language[message.chat.id] = 'en'
    else:
        user_language[message.chat.id] = 'ru'
    bot.reply_to(message, f'Language changed to {user_language[message.chat.id]}.')

# Функция отправки напоминаний
def send_reminders(chat_id):
    reminders = ["09:00", "12:00", "15:00", "18:00", "21:00"]
    while True:
        now = datetime.datetime.now().strftime('%H:%M')
        if now in reminders:
            bot.send_message(chat_id, texts[user_language[chat_id]]['reminder'])
            time.sleep(60)
        time.sleep(1)

bot.polling(none_stop=True)