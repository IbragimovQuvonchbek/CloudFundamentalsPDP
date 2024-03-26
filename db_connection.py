from datetime import datetime

from sqlalchemy import create_engine, String, Integer, DateTime, Boolean
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
    tg_id = mapped_column(String(20), unique=True)
    full_name = mapped_column(String(255))
    group_id = mapped_column(String(6))
    port = mapped_column(String(4), default=None)
    active = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=datetime.utcnow())


Base.metadata.create_all(engine)
