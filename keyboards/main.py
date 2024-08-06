from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅ Add new task', callback_data='create_task')],
        [InlineKeyboardButton(text='✔️ My tasks', callback_data='callback_tasks')],
        [InlineKeyboardButton(text='📝 My notes', callback_data='callback_tags')],
        [InlineKeyboardButton(text='📊 Currency rates', callback_data='callback_currency')],
        [InlineKeyboardButton(text='🔐 Password generator', callback_data='callback_password')],
    ]
)
