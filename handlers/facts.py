# handlers/facts.py

import random
from deep_translator import GoogleTranslator
import requests
import pytz
import datetime
from utils import get_user, error_handler
from global_vars import texts, bot, logger, active_threads

@bot.message_handler(commands=['fact'])
@error_handler
def fact_handler(message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    fact_text = ""
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en", timeout=10)
        if response.status_code == 200:
            data = response.json()
            fact_text = data.get("text", "")
        else:
            fact_text = random.choice(texts[user.language]["facts"])
    except Exception as e:
        logger.error(f"Ошибка при получении факта: {str(e)}", exc_info=True)
        fact_text = random.choice(texts[user.language]["facts"])

    if user.language == "ru" and fact_text:
        try:
            fact_text = GoogleTranslator(source='en', target='ru').translate(fact_text)
        except Exception as e:
            logger.error(f"Ошибка перевода факта: {str(e)}", exc_info=True)

    bot.send_message(chat_id, f"{texts[user.language]['fact']}\n{fact_text}")

    timezone = pytz.timezone(user.timezone)
    current_time = datetime.datetime.now(timezone).strftime("%H:%M")
    if chat_id in active_threads:
        active_threads[chat_id]["last_sent"] = current_time
