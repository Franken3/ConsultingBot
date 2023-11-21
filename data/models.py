import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import *
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, relationship

load_dotenv()
alchemy_engine = str(os.getenv("ALCHEMY_ENGINE"))


class Base(DeclarativeBase):
    pass


async def create_session():
    async_engine = create_async_engine(alchemy_engine)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return AsyncSession(async_engine)


# class Messages(Base):
#     __tablename__ = "Messages"
#     id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
#     msg_ids = Column(JSON)
#     order_id = Column(Text, primary_key=True, index=True)
#     merch_code = Column(Text, index=True, default=False)
#     store_id = Column(Text, index=True)
#     status = Column(Text)
#     paid = Column(BIGINT)
#     total = Column(BIGINT)
#     viaAlt = Column(Boolean)
#     errorCode = Column(INT)
#     errorMessage = Column(Text)
#     tableNumber = Column(Text)


class Users(Base):
    __tablename__ = "Users"
    tg_id = Column(BIGINT, primary_key=True, index=True)
    dialogs = relationship("UserDialogs", back_populates="user")


class UserDialogs(Base):
    __tablename__ = "UserDialogs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BIGINT, ForeignKey('Users.tg_id'))
    msg_id = Column(BIGINT)
    section = Column(Text, nullable=False)
    user_prompt = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    role = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("Users", back_populates="dialogs")

async def create_all():
    async_engine = create_async_engine(alchemy_engine)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return AsyncSession(async_engine)


if __name__ == "__main__":
    try:
        asyncio.run(create_all())
        print('Таблицы созданы успешно')
        T ="""⠄⠄⣿⣿⣿⣿⠘⡿⢛⣿⣿⣿⣿⣿⣧⢻⣿⣿⠃⠸⣿⣿⣿⠄⠄⠄⠄⠄ 
⠄⠄⣿⣿⣿⣿⢀⠼⣛⣛⣭⢭⣟⣛⣛⣛⠿⠿⢆⡠⢿⣿⣿⠄⠄⠄⠄⠄ 
⠄⠄⠸⣿⣿⢣⢶⣟⣿⣖⣿⣷⣻⣮⡿⣽⣿⣻⣖⣶⣤⣭⡉⠄⠄⠄⠄⠄ 
⠄⠄⠄⢹⠣⣛⣣⣭⣭⣭⣁⡛⠻⢽⣿⣿⣿⣿⢻⣿⣿⣿⣽⡧⡄⠄⠄⠄ 
⠄⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣶⣌⡛⢿⣽⢘⣿⣷⣿⡻⠏⣛⣀⠄⠄ 
⠄⠄⠄⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠙⡅⣿⠚⣡⣴⣿⣿⣿⡆⠄ 
⠄⠄⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⣱⣾⣿⣿⣿⣿⣿⣿⠄ 
⠄⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⠄ 
⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠣⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄ 
⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠑⣿⣮⣝⣛⠿⠿⣿⣿⣿⣿⠄ 
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟"""
        print(T)
    except Exception as e:
        print(f'Подготовка таблиц: {e}')
