from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b = {
    'ru': KeyboardButton(text='Русский'),
    'uz': KeyboardButton(text='Узбекский'),
    'contact_ru': KeyboardButton(text='Поделиться контактом', request_contact=True),
    'contact_uz': KeyboardButton(text="Kontaktni baham ko'ring", request_contact=True),
    'reg_and_ru': KeyboardButton(text='Андижанская область'),
    'reg_buh_ru': KeyboardButton(text='Бухарская область'),
    'reg_jiz_ru': KeyboardButton(text='Джизакская область'),
    'reg_kas_ru': KeyboardButton(text='Кашкадарьинская область'),
    'reg_nav_ru': KeyboardButton(text='Навоийская область'),
    'reg_nam_ru': KeyboardButton(text='Наманганская область'),
    'reg_kar_ru': KeyboardButton(text='Республика Каракалпакстан'),
    'reg_sam_ru': KeyboardButton(text='Самаркандская область'),
    'reg_sur_ru': KeyboardButton(text='Сурхандарьинская область'),
    'reg_sir_ru': KeyboardButton(text='Сырдарьинская область'),
    'reg_tas_ru': KeyboardButton(text='Ташкентская область'),
    'reg_fer_ru': KeyboardButton(text='Ферганская область'),
    'reg_hor_ru': KeyboardButton(text='Хорезмская область'),
    'reg_and_uz': KeyboardButton(text="Andijon viloyati"),
    'reg_buh_uz': KeyboardButton(text="Buxoro viloyati"),
    'reg_jiz_uz': KeyboardButton(text="Jizzax viloyati"),
    'reg_kas_uz': KeyboardButton(text="Qashqadaryo viloyati"),
    'reg_nav_uz': KeyboardButton(text="Navoiy viloyati"),
    'reg_nam_uz': KeyboardButton(text="Namangan viloyati"),
    'reg_kar_uz': KeyboardButton(text="Qoraqalpog’iston Respublikasi"),
    'reg_sam_uz': KeyboardButton(text="Samarqand viloyati"),
    'reg_sur_uz': KeyboardButton(text="Surxondaryo viloyati"),
    'reg_sir_uz': KeyboardButton(text="Sirdaryo viloyati"),
    'reg_tas_uz': KeyboardButton(text="Toshkent viloyati"),
    'reg_fer_uz': KeyboardButton(text="Farg’ona viloyati"),
    'reg_hor_uz': KeyboardButton(text="Xorazm viloyati"),
    'about_ru': KeyboardButton(text='О компании'),
    'about_uz': KeyboardButton(text="Kompaniya haqida"),
    'vacancies_list_ru': KeyboardButton(text='Список вакансий'),
    'vacancies_list_uz': KeyboardButton(text="Bo'sh ish o'rinlari ro'yxati"),
    'order_ru': KeyboardButton(text='Подать заявку'),
    'order_uz': KeyboardButton(text="Hozir murojaat qiling"),
}

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[b['ru'], b['uz']]])
contact_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[b['contact_ru']]])
contact_kb_uz = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[b['contact_uz']]])
regions_kb_ru = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [b['reg_and_ru'], b['reg_buh_ru']],
        [b['reg_jiz_ru'], b['reg_kas_ru']],
        [b['reg_nav_ru'], b['reg_nam_ru']],
        [b['reg_kar_ru'], b['reg_sam_ru']],
        [b['reg_sur_ru'], b['reg_sir_ru']],
        [b['reg_tas_ru'], b['reg_fer_ru']],
        [b['reg_hor_ru']]
    ]
)
regions_kb_uz = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [b['reg_and_uz'], b['reg_buh_uz']],
        [b['reg_jiz_uz'], b['reg_kas_uz']],
        [b['reg_nav_uz'], b['reg_nam_uz']],
        [b['reg_kar_uz'], b['reg_sam_uz']],
        [b['reg_sur_uz'], b['reg_sir_uz']],
        [b['reg_tas_uz'], b['reg_fer_uz']],
        [b['reg_hor_uz']]
    ]
)
main_menu_kb_ru = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [b['about_ru']],
        [b['vacancies_list_ru']],
        [b['order_ru']],
    ]
)
main_menu_kb_uz = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [b['about_uz']],
        [b['vacancies_list_uz']],
        [b['order_uz']],
    ]
)