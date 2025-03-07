# 💧 Water Reminder Bot 🌍

Умный телеграм-бот для персональных напоминаний о питьевом режиме с мультиязычной поддержкой и интеллектуальными функциями.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- ![Демонстрация работы бота](/demo.gif) -->

## 🌟 Уникальные возможности

- 🎯 Динамическая настройка расписания командой `/set_time`
- 🌍 Автоматическое определение и ручная установка часовых поясов
- 🔄 Интеллектуальный перевод фактов на выбранный язык
- ⚡ Асинхронная система напоминаний с управлением потоками
- 📊 Встроенная система мониторинга активности пользователей
- 🛡 Продвинутая обработка ошибок с детальным логированием

## 🚀 Мгновенный старт

### Необходимые компоненты
- Python 3.8+
- Аккаунт Telegram
- Токен бота от [@BotFather](https://t.me/BotFather)

### Установочные шаги

1. Клонируйте репозиторий:
```bash
git clone https://github.com/KVadim-K/Water-Reminder-Bot.git
cd Water-Reminder-Bot
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Создать файл окружения:
```bash
echo "TELEGRAM_BOT_TOKEN=ваш_токен" > .env
```

4. Запустить бота:
```bash
python main.py
```

## 🛠 Настройка

### Конфигурация времени
Измените время напоминаний в файле `main.py`:
```python
REMINDER_TIMES = ["08:00", "12:30", "15:00", "18:45", "21:15"]  # Ваше расписание
TIMEZONE = pytz.timezone("Europe/Moscow")  # Ваш часовой пояс
```

### Добавление фактов
Редактируйте список фактов в разделе `texts`:
```python
"facts": [
    "Новый факт 1",
    "Новый факт 2"
]
```
## 🔧 Персонализация
### Настройка расписания
#### Используйте команду в чате:
```bash
/set_time 08:00 12:30 15:00 18:45 21:15
```

### Выбор часового пояса
#### Установите предпочтительную зону:
```bash
/set_timezone Europe/Moscow
```

### Смена языка интерфейса
#### Переключитесь между языками:
```bash
/language
```

## 📜 Система команд

| Команда          | Описание                          | Пример использования       |
|------------------|-----------------------------------|----------------------------|
| `/start`         | Запуск/перезапуск бота            | `/start`                   |
| `/help`          | Справка по всем командам          | `/help`                    |
| `/fact`          | Получить случайный научный факт   | `/fact`                    |
| `/language`      | Переключить язык (ru/en)          | `/language`                |
| `/set_time`      | Установить время напоминаний      | `/set_time 09:00 13:00`    |
| `/set_timezone`  | Установить часовой пояс           | `/set_timezone Asia/Tokyo` |
| `/menu`          | Открыть главное меню              | `/menu`                    |
## 📌 Пример использования

1. Запустите бота командой:
```bash
/start
```

2. Получайте автоматические напоминания:
```
💧 Пора выпить стакан воды!
```

3. Запросите факт о воде:
```bash
/fact
```
Пример ответа:
```
🦈 Акулы используют воду для дыхания через жабры!
```
## 📸 Скриншоты

![Пример работы бота](/WRB1.PNG)

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

Разработано с ❤️ и 🚰 [KVadim-K](https://github.com/KVadim-K) | [Связаться](https://t.me/KVadim_K)
