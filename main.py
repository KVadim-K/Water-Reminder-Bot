import os
import logging
import threading
import datetime
import time
import random
import pytz
import functools
import requests
from deep_translator import GoogleTranslator  # Используем deep-translator для синхронного перевода

import telebot
from telebot import types  # Для создания кастомной клавиатуры
from dotenv import load_dotenv
from pathlib import Path
from models import Session, User, Admin

# Загрузка .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Инициализация бота
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Глобальный словарь для отслеживания потоков и времени последней отправки
active_threads = {}


# Декоратор для обработки ошибок
def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)

    return wrapper


# Вспомогательные функции
def get_user(chat_id):
    session = Session()
    try:
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(chat_id=chat_id)
            session.add(user)
            session.commit()
        return user
    finally:
        session.close()


def is_valid_time(time_str):
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


# Тексты для сообщений
texts = {
    "ru": {
        "welcome": "Привет! Я буду напоминать тебе пить воду!",
        "reminder": "💧 Пора выпить стакан воды!",
        "fact": "Лови случайный факт:",
        "help": ("Список команд:\n"
                 "/start - Запуск бота\n"
                 "/help - Справка\n"
                 "/fact - Случайный факт\n"
                 "/language - Смена языка\n"
                 "/set_time - Настроить время\n"
                 "/set_timezone - Установить часовой пояс\n"
                 "/menu - Главное меню"),
        "language_changed": "Язык изменен на русский",
        "time_updated": "⏰ Расписание обновлено!",
        "invalid_time": "❌ Неверный формат времени (используйте ЧЧ:ММ)",
        "facts": [
            "Интересный факт: Человек больше времени тратит на жевание, чем на сон.",
            "Интересный факт: Мёд никогда не портится.",
            "Интересный факт: У каждого человека уникальный запах тела."
        ],
    },
    "en": {
        "welcome": "Hello! I will remind you to drink water!",
        "reminder": "💧 Time to drink water!",
        "fact": "Random fact:",
        "help": ("Commands:\n"
                 "/start - Start bot\n"
                 "/help - Help\n"
                 "/fact - Random fact\n"
                 "/language - Change language\n"
                 "/set_time - Set schedule\n"
                 "/set_timezone - Set timezone\n"
                 "/menu - Main menu"),
        "language_changed": "Language changed to English",
        "time_updated": "⏰ Schedule updated!",
        "invalid_time": "❌ Invalid time format (use HH:MM)",
        "facts": [
            "Interesting fact: A human spends more time chewing than sleeping.",
            "Interesting fact: Honey never spoils.",
            "Interesting fact: Every person has a unique body odor."
        ],
    }
}


@bot.message_handler(commands=['set_timezone'])
@error_handler
def set_timezone_handler(message):
    chat_id = message.chat.id
    args = message.text.split()[1:]
    if not args:
        bot.send_message(chat_id, "❌ Укажите часовой пояс (например, Europe/London)")
        return
    timezone_str = args[0]
    if timezone_str not in pytz.all_timezones:
        bot.send_message(chat_id, "❌ Некорректный часовой пояс. Используйте, например, Europe/Moscow")
        return
    session = Session()
    try:
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(chat_id=chat_id, timezone=timezone_str)
            session.add(user)
        else:
            user.timezone = timezone_str
        session.commit()
        bot.send_message(chat_id, f"✅ Часовой пояс изменён на {timezone_str}")
    finally:
        session.close()


@bot.message_handler(commands=['start'])
@error_handler
def start_handler(message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    # Если для чата уже запущен reminder_loop – остановим его
    if chat_id in active_threads:
        active_threads[chat_id]["running"] = False
        time.sleep(3)
    # Инициализируем данные для данного чата
    active_threads[chat_id] = {"running": True, "last_sent": None}
    thread = threading.Thread(target=reminder_loop, args=(chat_id,), daemon=True)
    thread.start()
    bot.send_message(chat_id, texts[user.language]['welcome'])


def reminder_loop(chat_id):
    logger.info(f"Reminder loop started for chat_id={chat_id}")
    while active_threads.get(chat_id, {}).get("running", False):
        try:
            user = get_user(chat_id)
            reminder_times = set(user.reminder_times)
            timezone = pytz.timezone(user.timezone)
            now = datetime.datetime.now(timezone).strftime("%H:%M")
            last_sent = active_threads.get(chat_id, {}).get("last_sent")
            if now in reminder_times and now != last_sent:
                bot.send_message(chat_id, texts[user.language]["reminder"])
                active_threads[chat_id]["last_sent"] = now
            time.sleep(10)
        except Exception as e:
            logger.error(f"[reminder_loop] Ошибка: {str(e)}", exc_info=True)
            time.sleep(60)
    logger.info(f"Reminder loop stopped for chat_id={chat_id}")


@bot.message_handler(commands=['set_time'])
@error_handler
def set_time_handler(message):
    chat_id = message.chat.id
    times = message.text.split()[1:]
    if not times or not all(is_valid_time(t) for t in times):
        bot.send_message(chat_id, texts[get_user(chat_id).language]['invalid_time'])
        return
    session = Session()
    try:
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(chat_id=chat_id)
            session.add(user)
        user.reminder_times = times
        session.commit()
        bot.send_message(chat_id, texts[user.language]['time_updated'])
        logger.info(f"[set_time_handler] chat_id={chat_id}, новое расписание: {times}")
    finally:
        session.close()


@bot.message_handler(commands=['language'])
@error_handler
def language_handler(message):
    chat_id = message.chat.id
    session = Session()
    try:
        user = session.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(chat_id=chat_id)
            session.add(user)
        new_lang = "en" if user.language == "ru" else "ru"
        user.language = new_lang
        session.commit()
        bot.send_message(chat_id, texts[new_lang]['language_changed'])
    finally:
        session.close()


@bot.message_handler(commands=['help'])
@error_handler
def help_handler(message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    bot.send_message(chat_id, texts[user.language]['help'])


@bot.message_handler(commands=['menu'])
@error_handler
def menu_handler(message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    menu_text = "Выберите команду:" if user.language == "ru" else "Choose a command:"
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton("/start"), types.KeyboardButton("/fact"),
        types.KeyboardButton("/help"), types.KeyboardButton("/set_time"),
        types.KeyboardButton("/set_timezone"), types.KeyboardButton("/language")
    )
    bot.send_message(chat_id, menu_text, reply_markup=markup)


@bot.message_handler(commands=['fact'])
@error_handler
def fact_handler(message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    fact_text = ""
    try:
        # Используем API Useless Facts для получения случайного интересного факта
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=10)
        if response.status_code == 200:
            data = response.json()
            fact_text = data.get("text", "")
        else:
            fact_text = random.choice(texts[user.language]["facts"])
    except Exception as e:
        logger.error(f"Ошибка при получении факта: {str(e)}", exc_info=True)
        fact_text = random.choice(texts[user.language]["facts"])

    # Если язык установлен на русский — переводим факт
    if user.language == "ru" and fact_text:
        try:
            fact_text = GoogleTranslator(source='en', target='ru').translate(fact_text)
        except Exception as e:
            logger.error(f"Ошибка перевода факта: {str(e)}", exc_info=True)

    bot.send_message(chat_id, f"{texts[user.language]['fact']}\n{fact_text}")

    # Обновляем время последней отправки, чтобы избежать дублирования с напоминанием
    timezone = pytz.timezone(user.timezone)
    current_time = datetime.datetime.now(timezone).strftime("%H:%M")
    if chat_id in active_threads:
        active_threads[chat_id]["last_sent"] = current_time


@bot.message_handler(commands=['debug_info'])
@error_handler
def debug_info_handler(message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    logger.info(f"[debug_info_handler] chat_id={chat_id}, timezone={user.timezone}, times={user.reminder_times}")
    bot.send_message(chat_id, f"Твой часовой пояс: {user.timezone}\nТвоё расписание: {user.reminder_times}")


if __name__ == "__main__":
    logger.info("Бот запущен")
    bot.infinity_polling()
