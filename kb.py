from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b = {
    'ru': KeyboardButton(text='Русский'),
    'uz': KeyboardButton(text='Узбекский'),
    'contact_ru': KeyboardButton(text='Поделиться контактом', request_contact=True),
    'contact_uz': KeyboardButton(text="Kontaktni baham ko'ring", request_contact=True)
}

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[b['ru'], b['uz']]])
contact_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[b['contact_ru']]])
contact_kb_uz = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[b['contact_uz']]])
