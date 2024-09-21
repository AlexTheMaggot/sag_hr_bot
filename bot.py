import asyncio
from os import getenv

from aiogram import Dispatcher, Bot
from aiogram.client import bot
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
bot = None

class Menu(StatesGroup):
    lang = State()
    name = State()
    contact = State()
    region = State()
    custom_region = State()
    about = State()
    main_menu = State()
    about_us = State()
    vacancies_list = State()
    vacancies_detail = State()
    vacancies_order = State()
    order = State()
    change_lang = State()



@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    if not user_get_detail(message.chat.id):
        user_create(message.chat.id)
    await state.set_state(Menu.lang)
    text = "Вас приветствует HR-бот SAG Group. История SAG Group берет свое начало с создания фабрики по производству "
    text += "ковров в 2000 году. На данный момент в состав SAG Group входит более 10 компаний из различных сфер "
    text += "экономики, многие из которых являются лидерами в своих отраслях.\n\nПожалуйста, укажите язык.\n\n"
    text += "SAG Group HR botiga xush kelibsiz. SAG Group tarixi 2000 yilda gilam fabrikasining tashkil etilishidan "
    text += "boshlanadi. Ayni paytda SAG Group tarkibiga iqtisodiyotning turli tarmoqlaridan 10 dan ortiq kompaniyalar "
    text += "kiradi, ularning aksariyati o‘z sohalarida yetakchi hisoblanadi.\n\nIltimos, tilni tanlang."
    await message.answer(text, reply_markup=kb.start_kb)


@dp.message(Menu.lang)
async def language_handler(message: Message, state: FSMContext):
    match message.text:
        case 'Русский':
            user_update(message.chat.id, lang='ru')
            await state.set_state(Menu.name)
            await message.answer(text='Напишите, пожалуйста, ваше ФИО')
        case "O'zbek":
            user_update(message.chat.id, lang='uz')
            await state.set_state(Menu.name)
            await message.answer(text="Iltimos, FISh yozing.")
        case _:
            await message.answer(text='Пожалуйста укажите язык\n\nTilni belgilang', reply_markup=kb.start_kb)


@dp.message(Menu.name)
async def name_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    user_update(message.chat.id, name=message.text)
    await state.set_state(Menu.contact)
    if user['lang'] == 'ru':
        text = 'Предоставьте, пожалуйста, свои контактные данные.'
        contact_kb = kb.contact_kb_ru
    else:
        text = "Telefon raqamingizni qoldiring."
        contact_kb = kb.contact_kb_uz
    await message.answer(text=text, reply_markup=contact_kb)


@dp.message(Menu.contact)
async def contact_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    if message.contact:
        user_update(message.chat.id, phone_number=message.contact.phone_number)
        await state.set_state(Menu.region)
        if user['lang'] == 'ru':
            text = 'Пожалуйста, укажите ваш регион проживания.'
            regions_kb = kb.regions_kb_ru
        else:
            text = "Iltimos, yashash manzilingizni yozing."
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
        'Другой регион',
        "Boshqa mintaqa",
    ]
    if message.text in inputs:
        match message.text:
            case 'Другой регион':
                await state.set_state(Menu.custom_region)
                await message.answer(text='Пожалуйста напишите свой регион проживания')
            case "Boshqa mintaqa":
                await state.set_state(Menu.custom_region)
                await message.answer(text="Iltimos, yashash joyingizni yozing")
            case _:
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


@dp.message(Menu.custom_region)
async def custom_region_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    user_update(message.chat.id, region=message.text)
    await state.set_state(Menu.about)
    if user['lang'] == 'ru':
        text = 'Для завершения регистрации, расскажите пару слов о себе. '
        text += 'Можете указать род деятельности и/или ключевые навыки.'
    else:
        text = "Ro'yxatdan o'tishni yakunlash uchun bizga o'zingiz haqingizda bir necha so'z ayting. "
        text += "Siz o'zingizning faoliyat turini va/yoki asosiy ko'nikmalaringizni ko'rsatishingiz mumkin."
    await message.answer(text=text)


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
    match message.text:
        case 'О компании':
            await state.set_state(Menu.about_us)
            text = 'SAG - это лидирующее предприятие по производству ковров и ковровых изделий в Средней Азии, которое '
            text += 'было основано в 2000 году. На сегодняшний день, по производственным мощностям, SAG является самым '
            text += 'крупным предприятием на территории Средней Азии и стран СНГ.\n\nПредприятие начало свою '
            text += 'деятельность как небольшая ткацкая фабрика по производству ковров.На сегодняшний день все '
            text += 'процессы, начиная от производства нити заканчивая упаковкой конечной ковровой продукции '
            text += 'осуществляются на самом предприятии.Таким образом, SAG является одним из уникальных предприятий в '
            text += 'мире, где сконцентрирован весь производственный цикл.'
            keyboard = kb.back_kb_ru
        case 'Список вакансий':
            await state.set_state(Menu.vacancies_list)
            text = 'Выберите вакансию из списка ниже'
            keyboard = kb.vacancies_ru
        case 'Подать заявку':
            await state.set_state(Menu.order)
            text = 'Напишите комментарий к заявке'
            keyboard = kb.back_kb_ru
        case 'Сменить язык':
            await state.set_state(Menu.change_lang)
            text = 'Укажите язык'
            keyboard = kb.change_lang_kb_ru
        case "Kompaniya haqida":
            await state.set_state(Menu.about_us)
            text = "SAG 2000 - yilda tashkil etilgan bo’lib, Markaziy Osiyodagi yetakchi gilam ishlab chiqaruvchi "
            text += "kompaniya hisoblanadi.Bugungi kunda SAG ishlab chiqarish quvvati bo‘yicha Markaziy Osiyo va MDH "
            text += "mamlakatlaridagi eng yirik korxona hisoblanadi.\n\nKorxona o‘z faoliyatini gilam ishlab chiqarish "
            text += "bo‘yicha kichik to‘quv fabrikasi sifatida boshlagan. Bugungi kunda ip ishlab chiqarishdan tortib, "
            text += "tayyor gilam mahsulotlarini qadoqlashgacha bo‘lgan barcha jarayonlar korxonaning o‘zida amalga "
            text += "oshirilmoqda. Shunday qilib, SAG butun ishlab chiqarish tsikli jamlangan dunyodagi noyob "
            text += "kompaniyalardan biridir."
            keyboard = kb.back_kb_uz
        case "Bo'sh ish o'rinlari ro'yxati":
            await state.set_state(Menu.vacancies_list)
            text = "Quyidagi ro'yxatdan vakansiyani tanlang"
            keyboard = kb.vacancies_uz
        case "Hozir murojaat qiling":
            await state.set_state(Menu.order)
            text = "Ilovaga sharh yozing"
            keyboard = kb.back_kb_uz
        case "Tilni o'zgartirish":
            await state.set_state(Menu.change_lang)
            text = "Tilni ko'rsating"
            keyboard = kb.change_lang_kb_uz
        case _:
            if user['lang'] == 'ru':
                text = 'Пожалуйста, выберите пункт из меню ниже'
                keyboard = kb.main_menu_kb_ru
            else:
                text = "Quyidagi menyudan biror narsani tanlang"
                keyboard = kb.main_menu_kb_uz
    await message.answer(text=text, reply_markup=keyboard)


@dp.message(Menu.about_us)
async def about_us_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    if user['lang'] == 'ru':
        text = 'Главное меню'
        keyboard = kb.main_menu_kb_ru
    else:
        text = "Asosiy menyu"
        keyboard = kb.main_menu_kb_uz
    await state.set_state(Menu.main_menu)
    await message.answer(text=text, reply_markup=keyboard)


@dp.message(Menu.change_lang)
async def change_lang_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    match message.text:
        case 'Русский':
            user_update(message.chat.id, lang='ru')
            await state.set_state(Menu.main_menu)
            await message.answer('Язык изменен!', reply_markup=kb.main_menu_kb_ru)
        case "O'zbek":
            user_update(message.chat.id, lang="uz")
            await state.set_state(Menu.main_menu)
            await message.answer("Til o'zgartirildi!", reply_markup=kb.main_menu_kb_uz)
        case 'Назад':
            await state.set_state(Menu.main_menu)
            await message.answer('Главное меню', reply_markup=kb.main_menu_kb_ru)
        case "Orqaga":
            await state.set_state(Menu.main_menu)
            await message.answer("Asosiy menyu", reply_markup=kb.main_menu_kb_uz)
        case _:
            if user['lang'] == 'ru':
                await message.answer('Пожалуйста выберите язык из списка ниже.', reply_markup=kb.change_lang_kb_ru)
            else:
                await message.answer("Quyidagi roʻyxatdan tilni tanlang.", reply_markup=kb.change_lang_kb_uz)


@dp.message(Menu.order)
async def order_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    await state.set_state(Menu.main_menu)
    if message.text == 'Назад':
        await message.answer('Главное меню', reply_markup=kb.main_menu_kb_ru)
    elif message.text == "Orqaga":
        await message.answer('Asosiy menyu', reply_markup=kb.main_menu_kb_uz)
    else:
        text = 'Новая заявка!\n\n'
        text += f'Имя: {user["name"]}\n'
        text += f'Номер телефона: {user["phone_number"]}\n'
        text += f'Предпочитаемый язык: {'Русский' if user["lang"] == 'ru' else 'Узбекский'}\n'
        text += f'Регион: {user["region"]}\n'
        text += f'Дополнительная информация: {user["about"]}\n\n'
        text += f'Комментарий: {message.text}'
        await bot.send_message(chat_id=-1002456307374, text=text)
        if user['lang'] == 'ru':
            await message.answer('Ваша заявка отправлена', reply_markup=kb.main_menu_kb_ru)
        else:
            await message.answer("Sizning arizangiz yuborildi", reply_markup=kb.main_menu_kb_uz)


@dp.message(Menu.vacancies_list)
async def vacancies_list_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    match message.text:
        case 'Продавец-консультант (Ташкент)':
            await state.update_data({'vacancy': 'Продавец-консультант (Ташкент)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Обязанности:\n"
            text += "    консультирование покупателей;\n"
            text += "    продажа товара;\n"
            text += "    ведение отчетности;\n"
            text += "    поддержание чистоты в магазине.\n"
            text += "    участие в инвентаризации.\n\n"
            text += "🔸Требования:\n"
            text += "    опыт работы (приветствуется, но не обязателен);\n"
            text += "    знание узбекского и русского языка.\n"
            text += "    внимательность.\n"
            text += "    пунктуальность.\n\n"
            text += "🔹Условия:\n"
            text += "    График работы: с 9:00 до 19:00, 6 дней в неделю;\n"
            text += "    Обед за счет компании;\n"
            text += "    Адрес работы: Ташкент, улица Янги Сергели, 35\n"
            text += "    Профессиональный рост и развитие;\n"
            text += "    Дружелюбная и поддерживающая рабочая среда;\n"
            text += "    Официальное трудоустройство и социальные гарантии."
            keyboard = kb.vacancies_detail_kb_ru
        case 'Грузчик (Ташкент)':
            await state.update_data({'vacancy': 'Грузчик (Ташкент)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Обязанности:\n"
            text += "    Погрузка и выгрузка товаров;\n"
            text += "    Транспортировка грузов из одного места на другое;\n"
            text += "    Сортировка, упаковка и маркировка товаров и грузов перед отправкой;\n"
            text += "    Проверка состояния и количества поставленных грузов;\n"
            text += "    Выполнение задач по сопровождению грузов до их назначения.\n\n"
            text += "🔸Требования:\n"
            text += "    Трудолюбивость;\n"
            text += "    Коммуникабельность;\n"
            text += "    Ответственность;\n"
            text += "    Пунктуальность;\n"
            text += "    Стрессоустойчивость.\n\n"
            text += "🔹Условия:\n"
            text += "    График работы: с 9:00 до 19:00, 6 дней в неделю;\n"
            text += "    Обед за счет компании;\n"
            text += "    Профессиональный рост и развитие;\n"
            text += "    Дружелюбная и поддерживающая рабочая среда;\n"
            text += "    Официальное трудоустройство и социальные гарантии."
            keyboard = kb.vacancies_detail_kb_ru
        case 'Специалист по отделке края ковров (оверлок) (Ташкент)':
            await state.update_data({'vacancy': 'Специалист по отделке края ковров (оверлок) (Ташкент)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Обязанности:\n"
            text += "    Окантовка краев ковра на станке;\n"
            text += "    Содержание рабочего места в порядке после рабочего дня;\n"
            text += "    Регулярное техническое обслуживание машины, включая чистку и замену игл, ножей и других расходных частей;\n"
            text += "    Координация работы с другими членами команды, чтобы обеспечить своевременное выполнение заказов.\n\n"
            text += "🔸Требования:\n"
            text += "    Стрессоустойчивость;\n"
            text += "    Трудолюбие;\n"
            text += "    Готовность работать в команде;\n"
            text += "    Коммуникабельность;\n"
            text += "    Ответственность;\n"
            text += "    Пунктуальность.\n\n"
            text += "🔹Условия:\n"
            text += "    График работы: с 9:00 до 19:00, 6 дней в неделю;\n"
            text += "    Обед за счет компании;\n"
            text += "    Профессиональный рост и развитие;\n"
            text += "    Дружелюбная и поддерживающая рабочая среда;\n"
            text += "    Официальное трудоустройство и социальные гарантии."
            keyboard = kb.vacancies_detail_kb_ru
        case 'SMM-менеджер мобилограф (Самарканд)':
            await state.update_data({'vacancy': 'SMM-менеджер мобилограф (Самарканд)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Обязанности:\n"
            text += "    1. Управление социальными сетями:\n"
            text += "        Разработка и реализация стратегии продвижения в социальных сетях (Instagram, Facebook, и другие).\n"
            text += "        Создание и публикация оригинального контента, включая фото и видео, которые демонстрируют продукцию и рассказывают о нашем бренде.\n"
            text += "        Взаимодействие с аудиторией: ответ на комментарии и сообщения, проведение конкурсов и акций.\n"
            text += "    2. Контент-маркетинг:\n"
            text += "        Разработка и реализация контент-плана, включая статьи, блоги и другие материалы.\n"
            text += "        Работа с командой дизайнеров для создания визуальных материалов, соответствующих бренду.\n"
            text += "        Анализ эффективности контента и его оптимизация.\n"
            text += "    3. Планирование и реализация маркетинговых кампаний\n"
            text += "        Разработка и проведение рекламных кампаний, направленных на увеличение продаж и повышение узнаваемости бренда.\n"
            text += "        Анализ рынка и конкурентов для выявления новых возможностей и тенденций.\n"
            text += "        Подготовка отчетов о результатах кампаний и предложений по их улучшению.\n"
            text += "    4. Фотосъемка и видеосъемка:\n"
            text += "        Организация и проведение фотосессий и видеосъемок для продвижения продукции.\n"
            text += "        Пост-обработка и редактирование визуальных материалов.\n\n"
            text += "🔸Требования:\n"
            text += "    Опыт работы в маркетинге от 2-х лет, желательно в сфере розничной торговли или товаров для дома;\n"
            text += "    Умение работать с графическими редакторами (Adobe Photoshop, Illustrator и т.д.) и программами для редактирования видео;\n"
            text += "    Опыт управления социальными сетями и создания контента.\n\n"
            text += "🔹Условия:\n"
            text += "    Конкурентоспособная заработная плата.\n"
            text += "    Возможность профессионального и карьерного роста.\n"
            text += "    Дружелюбная команда и комфортные условия работы.\n"
            text += "    Возможность реализовать свои креативные идеи и проекты."
            keyboard = kb.vacancies_detail_kb_ru
        case 'Стажер HR-аналитик (Самарканд)':
            await state.update_data({'vacancy': 'Стажер HR-аналитик (Самарканд)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Обязанности:\n"
            text += "    -Формирование бюджета затрат на персонал, факторный анализ.\n"
            text += "    - Внедрение системы оплаты труда и премирования для компании на основе KPI.\n"
            text += "    -Ежемесячная отчетность о движении персонала, его качественной и количественной структуре, текучести кадров.\n"
            text += "    -Отчётность по укомплектованности/достаточности персонала.\n"
            text += "    -Анализ оттока персонала.\n"
            text += "    -Внедрение системы грейдов.\n"
            text += "🔸Требования:\n"
            text += "    -Высшее образование (экономическое, бухгалтерское, финансовое);\n"
            text += "    -Желателен опыт работы по направлению, но необязателен - всему обучим;\n"
            text += "    -Уверенный пользователь офисных программ (Excel, 1C).\n"
            text += "🔹Условия:\n"
            text += "    -Комфортабельный офис по адресу: Катта Узбек Тракт, 14;\n"
            text += "    -График работы 5/2 с 9:00 до 18:00;\n"
            text += "    -Оплачиваемая стажировка - 3 месяца, далее официальное оформление в штат;\n"
            text += "    -Транспорт и обед за счет компании;\n"
            text += "    -Возможность развития профессиональных навыков и приобретения ценного опыта."
            keyboard = kb.vacancies_detail_kb_ru
        case 'Аккаунт-менеджер (Ташкент)':
            await state.update_data({'vacancy': 'Аккаунт-менеджер (Ташкент)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Обязанности:\n"
            text += "    - Обработка обращений от клиентов (чаты в соц.сетях);\n"
            text += "    - Совершение исходящих звонков клиентам;\n"
            text += "    - Выстраивание долгосрочных отношений с клиентами;\n"
            text += "    - Консультирование и стимулирование клиентов к продажам.\n"
            text += "🔸Требования:\n"
            text += "    - Высшее образование;\n"
            text += "    - Опыт работы приветствуется, но необязателен;\n"
            text += "    - Желательно наличие профильных курсов;\n"
            text += "    - Уверенный пользователь ПК;\n"
            text += "    - Высокая скорость печати (мессенджеры, соц.сети);\n"
            text += "    - Владение русским и узбекским языками.\n"
            text += "🔹Условия:\n"
            text += "    - Официальное трудоустройство;\n"
            text += "    - Комфортабельный коворкинг по адресу: улица Богибустон, 186 (Impact Technology Hub);\n"
            text += "    - Возможность карьерного роста.\n"
            keyboard = kb.vacancies_detail_kb_ru
        case "Sotuvchi-maslahatchi (Toshkent)":
            await state.update_data({'vacancy': 'Продавец-консультант (Ташкент)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Mas'uliyat:\n"
            text += "    • mijozlarga maslahat berish;\n"
            text += "    • tovarlarni sotish;\n"
            text += "    • hisobot berish;\n"
            text += "    • do'konda tozalikni saqlash.\n"
            text += "    • inventarizatsiyada ishtirok etish.\n\n"
            text += "🔸Qo'yiladigan talablar:\n"
            text += "    • Ish tajribasi (ish tajribangiz bo’lsa u mamnuniyat bilan qabul qilinadi, lekin talab qilinmaydi);\n"
            text += "    • o'zbek va rus tillarini bilish.\n"
            text += "    • e'tiborli bo'lish.\n"
            text += "    • Punktual bo’lish.\n\n"
            text += "🔹Shartlar:\n"
            text += "    • Ish vaqti: 9:00 dan 19:00 gacha, haftasiga 6 kun;\n"
            text += "    • Tushlik kompaniya hisobidan;\n"
            text += "    • Ish manzili: Toshkent sh., Yangi Sergeli ko‘chasi, 35-uy\n"
            text += "    • Martaba o'sishi va rivojlanish;\n"
            text += "    • Do'stona va qo'llab-quvvatlovchi ish muhiti;\n"
            text += "    • Rasmiy bandlik va ijtimoiy kafolatlar."
            keyboard = kb.vacancies_detail_kb_uz
        case "Yuk tashuvchi (Toshkent)":
            await state.update_data({'vacancy': 'Грузчик (Ташкент)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Mas'uliyat:\n"
            text += "    • Tovarlarni yuklash va tushirish;\n"
            text += "    • yuklarni bir joydan ikkinchi joyga tashish;\n"
            text += "    • Yuk tashishdan oldin tovarlar va yuklarni saralash, qadoqlash va etiketlash;\n"
            text += "    • Yetkazib berilgan tovarlarning holati va miqdorini tekshirish;\n"
            text += "    • Yuklarni belgilangan joyga kuzatib borish bo'yicha vazifalarni bajarish.\n\n"
            text += "🔸Talablar:\n"
            text += "    • Mehnatsevarlik;\n"
            text += "    • Muloqot qobiliyati;\n"
            text += "    • Mas'uliyat;\n"
            text += "    • O’z vaqtida bo’lishlik;\n"
            text += "    • Stressga chidamlilik.\n\n"
            text += "🔹Shartlar:\n"
            text += "    • Ish vaqti: 9:00 dan 19:00 gacha, haftasiga 6 kun;\n"
            text += "    • Tushlik kompaniya hisobidan;\n"
            text += "    • Martaba o'sishi va rivojlanish;\n"
            text += "    • Do'stona va qo'llab-quvvatlovchi ish muhiti;\n"
            text += "    • Rasmiy bandlik va ijtimoiy kafolatlar."
            keyboard = kb.vacancies_detail_kb_uz
        case "Gilam chetlarini tikish bo‘yicha mutaxassis (overlok) (Toshkent)":
            await state.update_data({'vacancy': 'Специалист по отделке края ковров (оверлок) (Ташкент)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Ma’suliyat:\n"
            text += "    • Gilamning chetlarini stanokda qirqish;\n"
            text += "    • ish joyini tartibda saqlash;\n"
            text += "    • Stanokga muntazam texnik xizmat ko'rsatish, shu jumladan ignalar, pichoqlar va boshqa sarflanadigan qismlarni tozalash va almashtirish;\n"
            text += "    • Buyurtmalarning o'z vaqtida bajarilishini ta'minlash uchun boshqa jamoa a'zolari bilan birga ishlash.\n\n"
            text += "🔸Talablar:\n"
            text += "    • Mehnatsevarlik;\n"
            text += "    • Jamoada ishlash istagi;\n"
            text += "    • Muloqot qobiliyati;\n"
            text += "    • Mas'uliyat;\n"
            text += "    • O’z vaqtida bo’lishlik.\n\n"
            text += "🔹Sharoitlar:\n"
            text += "    • Ish vaqti: 9:00 dan 19:00 gacha, haftasiga 6 kun;\n"
            text += "    • Tushlik kompaniya hisobidan;\n"
            text += "    • Martaba o'sishi va rivojlanish;\n"
            text += "    • Do'stona va qo'llab-quvvatlovchi ish muhiti;\n"
            text += "    • Rasmiy bandlik va ijtimoiy kafolatlar."
            keyboard = kb.vacancies_detail_kb_uz
        case "SMM menejeri/mobilograf (Samarqand)":
            await state.update_data({'vacancy': 'SMM-менеджер мобилограф (Самарканд)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Mas'uliyat:\n"
            text += "    1. Ijtimoiy tarmoqlarni boshqarish:\n"
            text += "        • Ijtimoiy tarmoqlarda (Instagram, Facebook va boshqalar) reklama strategiyasini ishlab chiqish va amalga oshirish.\n"
            text += "        • Mahsulotlarni ko'rsatadigan va brendimiz haqida gapiradigan fotosuratlar va videolarni o'z ichiga olgan original kontentni yaratish va nashr etish.\n"
            text += "        • Tomoshabinlar bilan o'zaro aloqa: sharhlar va xabarlarga javob berish, tanlovlar va aksiyalarni o'tkazish.\n"
            text += "    2. Kontent marketingi:\n"
            text += "        • Maqolalar, bloglar va boshqa materiallarni o'z ichiga olgan kontent rejasini ishlab chiqish va amalga oshirish.\n"
            text += "        • Brendga mos keladigan visual materiallar yaratish uchun dizayn jamoasi bilan ishlash.\n"
            text += "        • Kontent samaradorligini tahlil qilish va uni optimallashtirish.\n"
            text += "    3. Marketing kampaniyalarini rejalashtirish va amalga oshirish\n"
            text += "        • savdo hajmini oshirish va brend xabardorligini oshirishga qaratilgan reklama kampaniyalarini ishlab chiqish va amalga oshirish.\n"
            text += "        • Yangi imkoniyatlar va tendentsiyalarni aniqlash uchun bozor va raqobatchilar tahlilini o’tkazish.\n"
            text += "        • Kampaniya natijalari bo‘yicha hisobotlar va ularni takomillashtirish bo‘yicha takliflar tayyorlash.\n"
            text += "    4. Fotografiya va videografiya:\n"
            text += "        • Mahsulotlarni reklama qilish uchun fotosessiyalar va videofilmlar tashkil etish va o‘tkazish.\n"
            text += "        • Vizual materiallarni qayta ishlash va tahrirlash.\n\n"
            text += "🔸Talablar:\n"
            text += "    • Marketing sohasida kamida 2 yillik ish tajribasi, donabay yoki uy-roʻzgʻor buyumlari sotish sohasida tajribangiz bo’lsa, mamnuniyat bilan qabul qilinadi;\n"
            text += "    • Grafik muharrirlar (Adobe Photoshop, Illustrator va boshqalar) va video tahrirlash dasturlari bilan ishlash qobiliyati;\n"
            text += "    • Ijtimoiy tarmoqlarni boshqarish va kontent yaratish tajribasi.\n\n"
            text += "🔹Sharoitlar:\n"
            text += "    • Raqobatbardosh ish haqi.\n"
            text += "    • Martaba o'sishi uchun imkoniyat.\n"
            text += "    • Do'stona va qo'llab-quvvatlovchi ish muhiti.\n"
            text += "    • Ijodiy g'oyalar va loyihalarni amalga oshirish imkoniyati."
            keyboard = kb.vacancies_detail_kb_uz
        case "HR-analitik stajyori (Samarkand)":
            await state.update_data({'vacancy': 'Стажер HR-аналитик (Самарканд)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Vazifalar:\n"
            text += "    - Xodimlar uchun xarajatlar byudjetini shakllantirish, faktorlash tahlili.\n"
            text += "    - KPI asosida kompaniya uchun mehnat haqini va mukofotlash tizimini joriy etish.\n"
            text += "    - Har oy xodimlar harakati, ularning sifat va miqdoriy tuzilishi, xodimlar oqimi bo‘yicha hisobot tayyorlash.\n"
            text += "    - Xodimlar soni/to‘g‘riligini bo‘yicha hisobot.\n"
            text += "    - Xodimlar oqimini tahlil qilish.\n"
            text += "    - Greyd tizimini joriy etish.\n"
            text += "🔸Talablar:\n"
            text += "    - Oliy ta’lim (iqtisodiyot, buxgalteriya, moliya).\n"
            text += "    - Yo‘nalish bo‘yicha ish tajribasi afzallik, ammo shart emas - hamma narsaga o‘rgatamiz.\n"
            text += "    - Ofis dasturlaridan (Excel, 1C) unumli foydalanish.\n"
            text += "🔹Sharoitlar:\n"
            text += "    - Manzil: Katta O‘zbekiston Trakt, 14, qulay ofis.\n"
            text += "    - Ish rejasi: 5/2, 09:00 dan 18:00 gacha.\n"
            text += "    - To‘lanadigan stajirovka - 3 oy, keyin rasmiy ishga qabul qilish.\n"
            text += "    - Transport va tushlik kompaniya hisobidan.\n"
            text += "    - Professional ko‘nikmalarni rivojlantirish va qimmatli tajriba orttirish imkoniyati.\n"
            keyboard = kb.vacancies_detail_kb_uz
        case "Akkaunt menejeri (Toshkent)":
            await state.update_data({'vacancy': 'Аккаунт-менеджер (Ташкент)'})
            await state.set_state(Menu.vacancies_detail)
            text = "🔸Mas'uliyat:\n"
            text += "    - mijozlar so'rovlarini qayta ishlash (ijtimoiy tarmoqlardagi chatlar);\n"
            text += "    - mijozlarga chiquvchi qo'ng'iroqlarni amalga oshirish;\n"
            text += "    - mijozlar bilan uzoq muddatli munosabatlarni o'rnatish;\n"
            text += "    - konsultatsiya va mijozlarni tovarni sotib olishi uchun rag'batlantirish.\n"
            text += "🔸Talablar:\n"
            text += "    - oliy ma'lumot;\n"
            text += "    - Ish tajribasi maqullanadi, lekin shart emas;\n"
            text += "    - Ixtisoslashtirilgan kurslarga ega bo'lish maqsadga muvofiq;\n"
            text += "    - Ishonchli kompyuter foydalanuvchisi;\n"
            text += "    - Tez matn yozish qobiliyati (messenjerlar, ijtimoiy tarmoqlar);\n"
            text += "    - Rus va o‘zbek tillarini bilish.\n"
            text += "🔹Sharoitlar:\n"
            text += "    - Rasmiy ish bilan taminlash;\n"
            text += "    - Bog‘ibuston ko‘chasi, 186-uyda (Impact Technology Hub) qulay kovorking maydoni;\n"
            text += "    - martaba o'sishi uchun imkoniyatlar.\n"
            keyboard = kb.vacancies_detail_kb_uz
        case "Назад":
            await state.set_state(Menu.main_menu)
            text = 'Главное меню'
            keyboard = kb.main_menu_kb_ru
        case "Orqaga":
            await state.set_state(Menu.main_menu)
            text = "Asosiy menyu"
            keyboard = kb.main_menu_kb_uz
        case _:
            if user['lang'] == 'ru':
                text = 'Пожалуйста выберите вакансию из списка ниже'
                keyboard = kb.vacancies_ru
            else:
                text = "Iltimos, quyidagi ro'yxatdan vakansiyani tanlang"
                keyboard = kb.vacancies_uz
    await message.answer(text=text, reply_markup=keyboard)


@dp.message(Menu.vacancies_detail)
async def vacancies_detail(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    match message.text:
        case "Подать заявку":
            await state.set_state(Menu.vacancies_order)
            text = "Укажите комментарий к заявке"
            keyboard = kb.back_kb_ru
        case "Назад":
            await state.set_state(Menu.vacancies_list)
            text = 'Список вакансий'
            keyboard = kb.vacancies_ru
        case "На главное меню":
            await state.set_state(Menu.main_menu)
            text = "Главное меню"
            keyboard = kb.main_menu_kb_ru
        case "Hozir murojaat qiling":
            await state.set_state(Menu.vacancies_order)
            text = "Iltimos, arizangizga sharh qoldiring"
            keyboard = kb.back_kb_uz
        case "Orqaga":
            await state.set_state(Menu.vacancies_list)
            text = "Bo'sh ish o'rinlari ro'yxati"
            keyboard = kb.vacancies_uz
        case "Asosiy menyuga":
            await state.set_state(Menu.main_menu)
            text = "Asosiy menyu"
            keyboard = kb.main_menu_kb_uz
        case _:
            if user['lang'] == 'ru':
                text = 'Пожалуйста выберите пункт ниже'
                keyboard = kb.vacancies_detail_kb_ru
            else:
                text = "Quyidagi elementni tanlang"
                keyboard = kb.vacancies_detail_kb_uz
    await message.answer(text=text, reply_markup=keyboard)


@dp.message(Menu.vacancies_order)
async def vacancies_order(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    match message.text:
        case 'Назад':
            await state.set_state(Menu.vacancies_list)
            text = "Список вакансий"
            keyboard = kb.vacancies_ru
        case "Orqaga":
            await state.set_state(Menu.vacancies_list)
            text = "Bo'sh ish o'rinlari ro'yxati"
            keyboard = kb.vacancies_uz
        case _:
            data = await state.get_data()
            order_text = 'Новая заявка!\n\n'
            order_text += f'Вакансия: {data["vacancy"]}\n'
            order_text += f'Имя: {user["name"]}\n'
            order_text += f'Номер телефона: {user["phone_number"]}\n'
            order_text += f'Предпочитаемый язык: {'Русский' if user["lang"] == 'ru' else 'Узбекский'}\n'
            order_text += f'Регион: {user["region"]}\n'
            order_text += f'Дополнительная информация: {user["about"]}\n\n'
            order_text += f'Комментарий: {message.text}'
            await bot.send_message(chat_id=-1002456307374, text=order_text)
            await state.set_state(Menu.main_menu)
            if user['lang'] == 'ru':
                text = 'Благодарим вас за предоставленную информацию. Сотрудники HR-отдела ознакомятся с вашей кандидатурой и вернутся с обратной связью!'
                keyboard = kb.main_menu_kb_ru
            else:
                text = "Berilgan ma’lumotlaringiz uchun rahmat. HR-bo'limi xodimlari sizning nomzodingizni ko'rib chiqadi va fikr-mulohazalarini bildiradi!"
                keyboard = kb.main_menu_kb_uz
    await message.answer(text=text, reply_markup=keyboard)



@dp.message()
async def echo_handler(message: Message, state: FSMContext):
    user = user_get_detail(message.chat.id)
    if not user:
        user_create(message.chat.id)
        await state.set_state(Menu.lang)
        text = "Вас приветствует HR-бот SAG Group. История SAG Group берет свое начало с создания фабрики по производству "
        text += "ковров в 2000 году. На данный момент в состав SAG Group входит более 10 компаний из различных сфер "
        text += "экономики, многие из которых являются лидерами в своих отраслях.\n\nПожалуйста, укажите язык.\n\n"
        text += "SAG Group HR botiga xush kelibsiz. SAG Group tarixi 2000 yilda gilam fabrikasining tashkil etilishidan "
        text += "boshlanadi. Ayni paytda SAG Group tarkibiga iqtisodiyotning turli tarmoqlaridan 10 dan ortiq kompaniyalar "
        text += "kiradi, ularning aksariyati o‘z sohalarida yetakchi hisoblanadi.\n\nIltimos, tilni tanlang."
        await message.answer(text, reply_markup=kb.start_kb)
    else:
        if user['about']:
            await state.set_state(Menu.main_menu)
            if user['lang'] == 'ru':
                await message.answer(text='Главное меню', reply_markup=kb.main_menu_kb_ru)
            else:
                await message.answer(text="Asosiy menyu", reply_markup=kb.main_menu_kb_uz)
        else:
            await state.set_state(Menu.lang)
            text = "Вас приветствует HR-бот SAG Group. История SAG Group берет свое начало с создания фабрики по производству "
            text += "ковров в 2000 году. На данный момент в состав SAG Group входит более 10 компаний из различных сфер "
            text += "экономики, многие из которых являются лидерами в своих отраслях.\n\nПожалуйста, укажите язык.\n\n"
            text += "SAG Group HR botiga xush kelibsiz. SAG Group tarixi 2000 yilda gilam fabrikasining tashkil etilishidan "
            text += "boshlanadi. Ayni paytda SAG Group tarkibiga iqtisodiyotning turli tarmoqlaridan 10 dan ortiq kompaniyalar "
            text += "kiradi, ularning aksariyati o‘z sohalarida yetakchi hisoblanadi.\n\nIltimos, tilni tanlang."
            await message.answer(text, reply_markup=kb.start_kb)


async def main():
    global bot
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
