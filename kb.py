from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b = {
    'ru': KeyboardButton(text='Русский'),
    'uz': KeyboardButton(text='Узбекский'),
}

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[[b['ru'], b['uz']]])
