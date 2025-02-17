# scheduler.py

import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from global_vars import bot, texts
from models import Session, Reminder, User

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def send_reminder(reminder_id, chat_id):
    session = Session()
    try:
        reminder = session.query(Reminder).filter_by(id=reminder_id, active=True).first()
        if reminder:
            user = session.query(User).filter_by(id=reminder.user_id).first()
            if user:
                bot.send_message(chat_id, texts[user.language]["reminder"])
                logger.info(f"Sent reminder for reminder_id={reminder_id} to chat_id={chat_id}")
    except Exception as e:
        logger.error(f"Error sending reminder: {e}", exc_info=True)
    finally:
        session.close()


def schedule_reminder(reminder):
    job_id = f"reminder_{reminder.id}"
    try:
        hour, minute = map(int, reminder.time.split(":"))
    except Exception as e:
        logger.error(f"Invalid time format for reminder {reminder.id}: {reminder.time}")
        return
    recurrence = reminder.recurrence.lower() if reminder.recurrence else "daily"

    if recurrence == "daily":
        scheduler.add_job(send_reminder,
                          'cron',
                          hour=hour,
                          minute=minute,
                          args=[reminder.id, reminder.user.chat_id],
                          id=job_id,
                          replace_existing=True)
        logger.info(f"Scheduled daily reminder job {job_id} for time {reminder.time}")
    elif recurrence == "weekly":
        # Используем день недели создания напоминания
        weekday = reminder.created_at.weekday()  # 0=Monday, 6=Sunday
        scheduler.add_job(send_reminder,
                          'cron',
                          day_of_week=weekday,
                          hour=hour,
                          minute=minute,
                          args=[reminder.id, reminder.user.chat_id],
                          id=job_id,
                          replace_existing=True)
        logger.info(f"Scheduled weekly reminder job {job_id} for time {reminder.time} on weekday {weekday}")
    else:
        logger.warning(
            f"Unknown recurrence type '{reminder.recurrence}' for reminder {reminder.id}. Defaulting to daily.")
        scheduler.add_job(send_reminder,
                          'cron',
                          hour=hour,
                          minute=minute,
                          args=[reminder.id, reminder.user.chat_id],
                          id=job_id,
                          replace_existing=True)
        logger.info(f"Scheduled default daily reminder job {job_id} for time {reminder.time}")


def unschedule_reminder(reminder_id):
    job_id = f"reminder_{reminder_id}"
    try:
        scheduler.remove_job(job_id)
        logger.info(f"Removed reminder job {job_id}")
    except Exception as e:
        logger.error(f"Error removing job {job_id}: {e}", exc_info=True)


def reschedule_reminder(reminder):
    unschedule_reminder(reminder.id)
    schedule_reminder(reminder)
