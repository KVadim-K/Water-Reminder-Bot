# config.py

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import telebot.apihelper as apihelper

# Загрузка .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Настройка кастомной сессии requests с повторными попытками
session_requests = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session_requests.mount("https://", adapter)
session_requests.mount("http://", adapter)

# Переопределяем глобальную сессию в telebot
apihelper._REQUEST_SESSION = session_requests

# Чтение токена из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
