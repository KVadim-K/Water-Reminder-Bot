# models.py

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    language = Column(String(2), default='ru')
    timezone = Column(String(50), default='Europe/Moscow')

    # Связь с напоминаниями
    reminders = relationship("Reminder", back_populates="user", cascade="all, delete-orphan")


class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    time = Column(String(5))  # формат "HH:MM"
    active = Column(Boolean, default=True)
    recurrence = Column(String(20), default=None)  # например, 'daily', 'weekly'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="reminders")


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)


# Используем expire_on_commit=False для избежания проблем с отсоединёнными объектами
engine = create_engine('sqlite:///bot_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)
