import os
import logging
import threading
import datetime
import time
import random
import pytz

import telebot
from dotenv import load_dotenv
from pathlib import Path

# Загрузка .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка токена
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("Токен не найден!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# Конфигурация
REMINDER_TIMES = ["08:00", "12:30", "15:00", "18:45", "21:15"]
TIMEZONE = pytz.timezone("Europe/Moscow")
user_language = {}
active_threads = {}

# Тексты
texts = {
    "ru": {
        "welcome": "Привет! Я буду напоминать тебе пить воду! Сейчас напоминания приходят в: " + ", ".join(
            REMINDER_TIMES),
        "reminder": "💧 Пора выпить стакан воды!",
        "fact": "Лови факт о воде:",
        "help": (
            "Список команд:\n"
            "/start - Запуск бота\n"
            "/help - Справка по командам\n"
            "/fact - Случайный факт о воде\n"
            "/language - Смена языка (ru/en)\n"
            "/test - Тестовое напоминание"
        ),
        "language_changed": "Язык изменен на русский",
        "facts": [
            "Человек может прожить без воды не более 3-4 дней.",
            "Вода покрывает около 71% поверхности Земли.",
            "Акулы используют воду для дыхания через жабры!",
            "Вода - единственное вещество, встречающееся в природе в трех состояниях."
        ],
    },
    "en": {
        "welcome": "Hello! I will remind you to drink water! Current schedule: " + ", ".join(REMINDER_TIMES),
        "reminder": "💧 Time to drink a glass of water!",
        "fact": "Here's a water fact:",
        "help": (
            "Available commands:\n"
            "/start - Start the bot\n"
            "/help - Show help\n"
            "/fact - Get a random water fact\n"
            "/language - Change language (ru/en)\n"
            "/test - Test reminder"
        ),
        "language_changed": "Language changed to English",
        "facts": [
            "A person can survive only 3-4 days without water.",
            "Water covers about 71% of Earth's surface.",
            "Sharks use water for breathing through gills!",
            "Water is the only substance found naturally in three states."
        ],
    }
}


def get_now():
    """Возвращает текущее время в заданном часовом поясе"""
    return datetime.datetime.now(TIMEZONE).strftime("%H:%M")


@bot.message_handler(commands=["start"])
def start_handler(message):
    """Обработчик команды /start"""
    chat_id = message.chat.id
    user_language[chat_id] = "ru"

    # Останавливаем предыдущий поток
    if chat_id in active_threads:
        active_threads[chat_id]["running"] = False

    # Запускаем новый поток
    active_threads[chat_id] = {"running": True}
    thread = threading.Thread(
        target=reminder_loop,
        args=(chat_id,),
        daemon=True
    )
    thread.start()

    bot.send_message(chat_id, texts["ru"]["welcome"])
    logger.info(f"Пользователь {chat_id} запустил бота")


def reminder_loop(chat_id):
    """Основной цикл напоминаний"""
    last_sent = None
    while active_threads.get(chat_id, {}).get("running", False):
        try:
            now = get_now()

            if now in REMINDER_TIMES and now != last_sent:
                lang = user_language.get(chat_id, "ru")
                bot.send_message(chat_id, texts[lang]["reminder"])
                logger.info(f"Отправлено напоминание {now} для {chat_id}")
                last_sent = now

                if random.random() < 0.3:
                    fact = random.choice(texts[lang]["facts"])
                    bot.send_message(chat_id, f"{texts[lang]['fact']}\n{fact}")

            time.sleep(10)

        except Exception as e:
            logger.error(f"Ошибка в потоке {chat_id}: {str(e)}")
            time.sleep(60)


@bot.message_handler(commands=["test"])
def test_handler(message):
    """Тестовая команда"""
    chat_id = message.chat.id
    lang = user_language.get(chat_id, "ru")
    bot.send_message(chat_id, texts[lang]["reminder"])
    logger.info(f"Тестовое напоминание отправлено {chat_id}")


@bot.message_handler(commands=["help"])
def help_handler(message):
    """Обработчик команды /help"""
    chat_id = message.chat.id
    lang = user_language.get(chat_id, "ru")
    bot.send_message(chat_id, texts[lang]["help"])


@bot.message_handler(commands=["fact"])
def fact_handler(message):
    """Обработчик команды /fact"""
    chat_id = message.chat.id
    lang = user_language.get(chat_id, "ru")
    fact = random.choice(texts[lang]["facts"])
    bot.send_message(chat_id, f"{texts[lang]['fact']}\n{fact}")


@bot.message_handler(commands=["language"])
def language_handler(message):
    """Обработчик команды /language"""
    chat_id = message.chat.id
    current_lang = user_language.get(chat_id, "ru")
    new_lang = "en" if current_lang == "ru" else "ru"
    user_language[chat_id] = new_lang
    bot.send_message(chat_id, texts[new_lang]["language_changed"])


if __name__ == "__main__":
    logger.info("Бот запущен")
    bot.infinity_polling()