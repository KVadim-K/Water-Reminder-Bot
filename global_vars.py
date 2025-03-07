# global_vars.py

from config import TOKEN, logger
import telebot

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Глобальный словарь для отслеживания потоков (для логики напоминаний, если нужна)
active_threads = {}

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
                 "/add_reminder - Добавить напоминание\n"
                 "/delete_reminder - Удалить напоминание\n"
                 "/update_reminder - Обновить напоминание\n"
                 "/list_reminders - Список напоминаний\n"
                 "/language - Смена языка\n"
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
                 "/add_reminder - Add reminder\n"
                 "/delete_reminder - Delete reminder\n"
                 "/update_reminder - Update reminder\n"
                 "/list_reminders - List reminders\n"
                 "/language - Change language\n"
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
