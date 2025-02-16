# main.py

from config import logger
from global_vars import bot
# Импорт обработчиков для регистрации команд в боте через декораторы
import handlers.reminder
import handlers.facts
import handlers.settings

if __name__ == "__main__":
    logger.info("Бот запущен")
    bot.infinity_polling()
