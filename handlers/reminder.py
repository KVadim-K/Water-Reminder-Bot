# handlers/reminder.py

import time
import datetime
import pytz
from models import Session, User, Reminder
from utils import get_user, is_valid_time, error_handler
from global_vars import logger, texts, bot, active_threads
from scheduler import schedule_reminder, unschedule_reminder, reschedule_reminder

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
    session_db = Session()
    try:
        user = session_db.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(chat_id=chat_id, timezone=timezone_str)
            session_db.add(user)
        else:
            user.timezone = timezone_str
        session_db.commit()
        bot.send_message(chat_id, f"✅ Часовой пояс изменён на {timezone_str}")
    finally:
        session_db.close()


@bot.message_handler(commands=['set_time'])
@error_handler
def set_time_handler(message):
    chat_id = message.chat.id
    times = message.text.split()[1:]
    if not times or not all(is_valid_time(t) for t in times):
        bot.send_message(chat_id, texts[get_user(chat_id).language]['invalid_time'])
        return
    session_db = Session()
    try:
        user = session_db.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(chat_id=chat_id)
            session_db.add(user)
        # Удаляем старые напоминания для пользователя
        session_db.query(Reminder).filter_by(user_id=user.id).delete()
        for t in times:
            reminder = Reminder(user_id=user.id, time=t, active=True)
            session_db.add(reminder)
            session_db.flush()  # чтобы reminder.id заполнился
            schedule_reminder(reminder)
        session_db.commit()
        bot.send_message(chat_id, texts[user.language]['time_updated'])
        logger.info(f"[set_time_handler] chat_id={chat_id}, новое расписание: {times}")
    finally:
        session_db.close()


@bot.message_handler(commands=['start'])
@error_handler
def start_handler(message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    # Мы больше не запускаем локальный цикл, чтобы избежать дублирования напоминаний.
    bot.send_message(chat_id, texts[user.language]['welcome'])
