from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Check your tasks', callback_data='callback_tasks')],
        [InlineKeyboardButton(text='Your notes', callback_data='callback_tags')],
        [InlineKeyboardButton(text='Get currency rates', callback_data='callback_currency')],
        [InlineKeyboardButton(text='Generate password', callback_data='callback_password')],
    ]
)
