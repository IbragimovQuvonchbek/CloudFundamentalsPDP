from datetime import datetime

from sqlalchemy import create_engine, String, Integer, DateTime, Boolean, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column

engine = create_engine('sqlite:///aiogram.db', echo=True)
Base = declarative_base()


class Task(Base):
    __tablename__ = 'taks'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(255))
    created_at = mapped_column(DateTime, default=datetime.utcnow)


class Student(Base):
    __tablename__ = 'student'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name = mapped_column(String(50))
    last_name = mapped_column(String(50))
    group_number = mapped_column(String(15))
    port_number = mapped_column(SmallInteger, default=5000)
    telegram_id = mapped_column(String(50))
    status = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow())


Base.metadata.create_all(engine)
