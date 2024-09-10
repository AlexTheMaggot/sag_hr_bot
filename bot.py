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
    region = State()
    about = State()
    main_menu = State()
    about_us = State()
    vacancies_list = State()
    order = State()
    change_lang = State()



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
        case "O'zbek":
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


@dp.message(Menu.contact)
async def contact_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    if message.contact:
        user_update(message.chat.id, phone_number=message.contact.phone_number)
        await state.set_state(Menu.region)
        if user['lang'] == 'ru':
            text = 'Пожалуйста, укажите регион проживания'
            regions_kb = kb.regions_kb_ru
        else:
            text = "Iltimos, yashash hududingizni ko'rsating"
            regions_kb = kb.regions_kb_uz
        await message.answer(text=text, reply_markup=regions_kb)
    else:
        if user['lang'] == 'ru':
            text = 'Пожалуйста нажмите на кнопку для того, чтобы поделиться контактом'
            keyboard = kb.contact_kb_ru
        else:
            text = "Yuborish Iltimos, kontaktni almashish uchun tugmani bosing"
            keyboard = kb.contact_kb_uz
        await message.answer(text=text, reply_markup=keyboard)


@dp.message(Menu.region)
async def region_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    inputs = [
        'Андижанская область',
        'Бухарская область',
        'Джизакская область',
        'Кашкадарьинская область',
        'Навоийская область',
        'Наманганская область',
        'Республика Каракалпакстан',
        'Самаркандская область',
        'Сурхандарьинская область',
        'Сырдарьинская область',
        'Ташкентская область',
        'Ферганская область',
        'Хорезмская область',
        "Andijon viloyati",
        "Buxoro viloyati",
        "Jizzax viloyati",
        "Qashqadaryo viloyati",
        "Navoiy viloyati",
        "Namangan viloyati",
        "Qoraqalpog’iston Respublikasi",
        "Samarqand viloyati",
        "Surxondaryo viloyati",
        "Sirdaryo viloyati",
        "Toshkent viloyati",
        "Farg’ona viloyati",
        "Xorazm viloyati",
    ]
    if message.text in inputs:
        user_update(message.chat.id, region=message.text)
        await state.set_state(Menu.about)
        if user['lang'] == 'ru':
            text = 'Для завершения регистрации, расскажите пару слов о себе. '
            text += 'Можете указать род деятельности и/или ключевые навыки.'
        else:
            text = "Ro'yxatdan o'tishni yakunlash uchun bizga o'zingiz haqingizda bir necha so'z ayting. "
            text += "Siz o'zingizning faoliyat turini va/yoki asosiy ko'nikmalaringizni ko'rsatishingiz mumkin."
        await message.answer(text=text)
    else:
        if user['lang'] == 'ru':
            text = 'Пожалуйста выберите регион из списка ниже.'
            regions_kb = kb.regions_kb_ru
        else:
            text = "Quyidagi roʻyxatdan hududingizni tanlang."
            regions_kb = kb.regions_kb_uz
        await message.answer(text=text, reply_markup=regions_kb)


@dp.message(Menu.about)
async def about_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    user_update(message.chat.id, about=message.text)
    await state.set_state(Menu.main_menu)
    if user['lang'] == 'ru':
        text = 'Регистрация завершена!'
        main_menu_kb = kb.main_menu_kb_ru
    else:
        text = "Roʻyxatdan oʻtish tugallandi!"
        main_menu_kb = kb.main_menu_kb_uz
    await message.answer(text=text, reply_markup=main_menu_kb)


@dp.message(Menu.main_menu)
async def main_menu_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    if user['lang'] == 'ru':
        match message.text:
            case 'О компании':
                await state.set_state(Menu.about_us)
                text = 'Текст описания о компании'
                keyboard = kb.back_kb_ru
            case 'Список вакансий':
                await state.set_state(Menu.vacancies_list)
                text = 'Выберите вакансию из списка ниже'
                keyboard = kb.back_kb_ru
            case 'Подать заявку':
                await state.set_state(Menu.order)
                text = 'Напишите комментарий к заявке'
                keyboard = kb.back_kb_ru
            case 'Сменить язык':
                await state.set_state(Menu.change_lang)
                text = 'Пожалуйста, укажите язык'
                keyboard = kb.change_lang_kb_ru
            case _:
                text = 'Пожалуйста, выберите пункт из меню ниже'
                keyboard = kb.main_menu_kb_ru
    else:
        match message.text:
            case "Kompaniya haqida":
                await state.set_state(Menu.about_us)
                text = "Kompaniya haqida tavsif matni"
                keyboard = kb.back_kb_uz
            case "Bo'sh ish o'rinlari ro'yxati":
                await state.set_state(Menu.vacancies_list)
                text = "Quyidagi ro'yxatdan vakansiyani tanlang"
                keyboard = kb.back_kb_uz
            case "Hozir murojaat qiling":
                await state.set_state(Menu.order)
                text = "Ilovaga sharh yozing"
                keyboard = kb.back_kb_uz
            case "Tilni o'zgartirish":
                await state.set_state(Menu.change_lang)
                text = "Tilni ko'rsating"
                keyboard = kb.change_lang_kb_uz
            case _:
                text = "Quyidagi menyudan biror narsani tanlang"
                keyboard = kb.main_menu_kb_ru
    await message.answer(text=text, reply_markup=keyboard)



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