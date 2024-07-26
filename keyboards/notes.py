from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Some catalog', callback_data='catalog')],
    [InlineKeyboardButton(text='Basket', callback_data='basket'),
     InlineKeyboardButton(text='Contacts', callback_data='contacts')]
])

settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='some text', url='https://www.youtube.com/')],
        [InlineKeyboardButton(text='text', url='https://docs.aiogram.dev/uk-ua/latest/migration_2_to_3.html')]
    ]
)

cars = ['Tesla', 'BMW', 'Opel', 'Tesla', 'BMW', 'Opel', 'Tesla', 'BMW', 'Opel', ]


async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(InlineKeyboardButton(text=car, url='https://www.youtube.com/'))
    return keyboard.adjust(2).as_markup()
