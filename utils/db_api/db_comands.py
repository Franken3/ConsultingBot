import os
from contextlib import asynccontextmanager
from copy import copy

from dotenv import load_dotenv
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from data.models import Users, UserDialogs

load_dotenv()
alchemy_engine = str(os.getenv("ALCHEMY_ENGINE"))

async_engine = create_async_engine(alchemy_engine)
AsyncSessionFactory = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session


async def save_user(tg_id) -> None:
    async with get_async_session() as session:
        stmp = select(Users).where(Users.tg_id == tg_id)
        result = await session.execute(stmp)
        user = result.scalar_one_or_none()
        if user is None:
            user: Users = Users(tg_id=tg_id)
            session.add(user)
        await session.commit()


async def get_user_dialog_history(tg_id: int) -> list:
    async with get_async_session() as session:
        stmt = select(UserDialogs).where(UserDialogs.user_id == tg_id).order_by(UserDialogs.timestamp)
        result = await session.execute(stmt)
        dialog_history = result.scalars().all()
        return [{"role": message.role, "content": message.message} for message in dialog_history]


async def save_user_and_assist_msg(user_message, assistant_message, msg_id, user_prompt, section, tg_id: int) -> None:
    async with get_async_session() as session:
        stmt = select(UserDialogs).where(and_(UserDialogs.user_id == tg_id))
        result = await session.execute(stmt)
        msgs = result.fetchall()
        if len(msgs) != 0:
            for msg in msgs:
                await session.delete(msg[0])
        new_user_message = UserDialogs(user_id=tg_id, message=user_message, role="user", msg_id=msg_id,
                                       user_prompt=user_prompt, section=section)

        new_assistant_message = UserDialogs(user_id=tg_id, message=assistant_message, role="assistant", msg_id=msg_id,
                                            user_prompt=user_prompt, section=section)
        session.add_all([new_user_message, new_assistant_message])
        await session.commit()


async def save_continue_answ(assistant_message, msg_id, tg_id: int) -> None:
    async with get_async_session() as session:
        print('save save save', msg_id, tg_id)
        stmt = select(UserDialogs).where(
            and_(UserDialogs.user_id == tg_id, UserDialogs.msg_id == msg_id, UserDialogs.role == 'assistant'))
        result = await session.execute(stmt)
        msg: UserDialogs = result.scalar_one_or_none()
        msg.message += assistant_message
        await session.commit()


async def get_assistant_answ(msg_id, tg_id: int) -> UserDialogs:
    async with get_async_session() as session:
        stmt = select(UserDialogs).where(
            and_(UserDialogs.user_id == tg_id, UserDialogs.msg_id == msg_id, UserDialogs.role == 'assistant'))
        result = await session.execute(stmt)
        msg: UserDialogs = result.scalar_one_or_none()
        r = copy(msg)

        stmt = select(UserDialogs).where(and_(UserDialogs.user_id == tg_id))
        result = await session.execute(stmt)
        msgs = result.fetchall()
        if len(msgs) != 0:
            for msg in msgs:
                await session.delete(msg[0])

        await session.commit()
        return r
