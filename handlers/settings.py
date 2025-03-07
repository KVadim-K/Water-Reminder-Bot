# handlers/settings.py

from utils import get_user, error_handler
from global_vars import texts, bot, logger
from telebot import types

@bot.message_handler(commands=['language'])
@error_handler
def language_handler(message):
    chat_id = message.chat.id
    from models import Session, User  # Импорт здесь для избежания циклических зависимостей
    session_db = Session()
    try:
        user = session_db.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(chat_id=chat_id)
            session_db.add(user)
        new_lang = "en" if user.language == "ru" else "ru"
        user.language = new_lang
        session_db.commit()
        bot.send_message(chat_id, texts[new_lang]['language_changed'])
    finally:
        session_db.close()


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


@bot.message_handler(commands=['debug_info'])
@error_handler
def debug_info_handler(message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    logger.info(f"[debug_info_handler] chat_id={chat_id}, timezone={user.timezone}")
    bot.send_message(chat_id, f"Твой часовой пояс: {user.timezone}\n")
