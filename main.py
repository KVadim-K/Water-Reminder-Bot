# main.py

from config import logger
from global_vars import bot
# Импорт обработчиков для регистрации команд
import handlers.reminder
import handlers.facts
import handlers.settings
import scheduler

if __name__ == "__main__":
    logger.info("Бот запущен")
    scheduler.scheduler.start()
    bot.infinity_polling()
