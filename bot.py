import asyncio
from os import getenv

from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import kb
from config import *


TOKEN = TELEGRAM_TOKEN
dp = Dispatcher()


class Menu(StatesGroup):
    lang = State()
    name = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    await state.set_state(Menu.lang)
    await message.answer('Приветствие и выбор языка', reply_markup=kb.start_kb)


@dp.message(Menu.lang)
async def language_handler(message: Message, state: FSMContext):
    match message.text:
        case 'Русский':
            await state.update_data(lang='ru')
            await state.set_state(Menu.name)
            await message.answer(text='Пожалуйста, укажите имя')
        case 'Узбекский':
            await state.update_data(lang='uz')
            await state.set_state(Menu.name)
            await message.answer(text='Пожалуйста, укажите имя(на узбекском)')
        case _:
            await message.answer(text='Пожалуйста укажите язык (рус и узб)', reply_markup=kb.start_kb)


@dp.message()
async def echo_handler(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Error')


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())