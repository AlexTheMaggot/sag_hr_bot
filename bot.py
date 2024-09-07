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
from db import *


TOKEN = TELEGRAM_TOKEN
dp = Dispatcher()


class Menu(StatesGroup):
    lang = State()
    name = State()
    contact = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    if not user_get_detail(message.chat.id):
        user_create(message.chat.id)
    await state.set_state(Menu.lang)
    text = "Вас приветствует HR-бот компании SAG. Пожалуйста, укажите язык:\n\n"
    text += "SAG HR botiga xush kelibsiz. Iltimos, tilingizni ko'rsating:"
    await message.answer(text, reply_markup=kb.start_kb)


@dp.message(Menu.lang)
async def language_handler(message: Message, state: FSMContext):
    match message.text:
        case 'Русский':
            user_update(message.chat.id, lang='ru')
            await state.set_state(Menu.name)
            await message.answer(text='Пожалуйста, укажите имя')
        case 'Узбекский':
            user_update(message.chat.id, lang='uz')
            await state.set_state(Menu.name)
            await message.answer(text="Iltimos, ismingizni kiriting")
        case _:
            await message.answer(text='Пожалуйста укажите язык\n\nTilni belgilang', reply_markup=kb.start_kb)


@dp.message(Menu.name)
async def name_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    user_update(message.chat.id, name=message.text)
    await state.set_state(Menu.contact)
    if user['lang'] == 'ru':
        text = 'Предоставьте, пожалуйста, свои контактные данные'
        contact_kb = kb.contact_kb_ru
    else:
        text = "Iltimos, aloqa ma'lumotlaringizni kiriting"
        contact_kb = kb.contact_kb_uz
    await message.answer(text=text, reply_markup=contact_kb)


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