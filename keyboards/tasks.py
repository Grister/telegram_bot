from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


async def goal_after_creating(goal_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Add monthly task', callback_data=f'create_monthly_task_{goal_id}')],
            [InlineKeyboardButton(text='Add other goal', callback_data='create_year_task')],
            [InlineKeyboardButton(text='Back to main', callback_data='#TODO')]
        ]
    )
