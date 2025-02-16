# utils.py

import datetime
import functools
from models import Session, User


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)}")

    return wrapper


def get_user(chat_id):
    session_db = Session()
    try:
        user = session_db.query(User).filter_by(chat_id=chat_id).first()
        if not user:
            user = User(chat_id=chat_id)
            session_db.add(user)
            session_db.commit()
        return user
    finally:
        session_db.close()


def is_valid_time(time_str):
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False
