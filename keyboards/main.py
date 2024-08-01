from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Check your tasks', callback_data='tasks'),
         KeyboardButton(text='Your notes', callback_data='notes')],
        [KeyboardButton(text='Currency', callback_data='Currency'),
         KeyboardButton(text='Generate password', callback_data='password')],
    ],
    resize_keyboard=True
)
