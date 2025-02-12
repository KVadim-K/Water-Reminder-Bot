from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    language = Column(String(2), default='ru')
    reminder_times = Column(JSON, default=lambda: ["08:00", "12:30", "15:00", "18:45", "21:15"])
    timezone = Column(String(50), default='Europe/Moscow')

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)

engine = create_engine('sqlite:///bot_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
