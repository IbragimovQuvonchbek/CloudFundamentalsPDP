from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from os import environ
from aiogram import Bot, Dispatcher, F
from aiogram import types
from aiogram.filters import CommandStart, Command
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType
from db_connection import engine, Task
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from aiogram.utils.markdown import hbold
from redis.asyncio import Redis
import asyncio
import logging
import sys

load_dotenv()

TOKEN = environ.get('TOKEN')
r = Redis(host='localhost', port=6379)
dp = Dispatcher(storage=RedisStorage(redis=r))


@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(f"Hello {hbold(message.from_user.full_name)}\nTo solve task send /tasks")


@dp.message(Command('tasks'))
async def text(message: types.Message) -> None:
    with Session(engine) as session:
        total_count = session.query(func.count(Task.id)).scalar()
        data = session.scalars(select(Task).limit(10).offset(10)).all()
        count = 0
        print(total_count)
        builder = InlineKeyboardBuilder()
        caption = ""
        for task in data:
            count += 1
            builder.button(text=f"{count}", callback_data=f"button_{task.id}")
            caption += f"{count}. {task.name}\n"
        if count == 0:
            await message.answer("Sorry, I couldn't find", reply_markup=builder.as_markup())
        else:

            if total_count > 10:
                builder.button(text='>>',
                               callback_data=f'forward_0_{message.text.lower()}')
            elif total_count > 20:
                builder.button(text='<<',
                               callback_data=f'back_0_{message.text.lower()}')
                builder.button(text='>>',
                               callback_data=f'forward_0_{message.text.lower()}')
            elif total_count < 20:
                builder.button(text='<<',
                               callback_data=f'back_0_{message.text.lower()}')
            builder.adjust(5, repeat=True)
            await message.answer(caption, reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith('forward_'))
async def forward(callback: types.CallbackQuery) -> None:
    data_arr = callback.data.split('_')
    fw = int(data_arr[-1]) + 10
    with Session(engine) as session:
        total_count = session.scalar(select(func.count(Task.id)))
        data = session.scalars(select(Task).limit(10).offset(fw)).all()
        builder = InlineKeyboardBuilder()
        caption = ""
        count = fw
        for task in data:
            count += 1
            builder.button(text=f"{count}", callback_data=f"button_{task.id}")
            caption += f"{count}. {task.name}\n"
        if count == 0:
            await callback.message.edit_text("Sorry, I couldn't find", reply_markup=builder.as_markup())
        else:
            if fw == 0 and fw > 10:
                builder.button(text='>>',
                               callback_data=f'forward_{fw}')
            elif fw != 0 and total_count > fw + 10:
                builder.button(text='<<',
                               callback_data=f'back_{fw}')
                builder.button(text='>>',
                               callback_data=f'forward_{fw}')
            elif fw != 0 and total_count < fw + 10:
                builder.button(text='<<',
                               callback_data=f'back_{fw}')
            builder.adjust(5, repeat=True)
            await callback.message.edit_text(caption, reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith('back_'))
async def back_callback(callback: types.CallbackQuery) -> None:
    data_arr = callback.data.split('_')
    bc = int(data_arr[-1]) - 10
    with Session(engine) as session:
        total_count = session.scalar(select(func.count(Task.id)))
        data = session.scalars(select(Task).limit(10).offset(bc)).all()
        builder = InlineKeyboardBuilder()
        caption = ""
        count = bc
        for task in data:
            count += 1
            builder.button(text=f"{count}", callback_data=f"button_{task.id}")
            caption += f"{count}. {task.name}\n"
        if count == 0:
            await callback.message.edit_text("Sorry, I couldn't find", reply_markup=builder.as_markup())
        else:
            if bc == 0 and total_count > 10:
                builder.button(text='>>',
                               callback_data=f'forward_{bc}')
            elif bc != 0 and total_count > bc + 10:
                builder.button(text='<<',
                               callback_data=f'back_{bc}')
                builder.button(text='>>',
                               callback_data=f'forward_{bc}')
            elif bc != 0 and total_count < bc + 10:
                builder.button(text='<<',
                               callback_data=f'back_{bc}')
            builder.adjust(5, repeat=True)
            await callback.message.edit_text(caption, reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith('button_'))
async def callback_query(callback: types.CallbackQuery) -> None:
    q_id = int(callback.data.split('_')[-1])
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == q_id).first()
        if task:
            await callback.message.answer(task.name)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
