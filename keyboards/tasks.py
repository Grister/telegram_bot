from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

empty_goals_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🎯 Add year goal', callback_data='create_year_task')],
        [InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start')]
    ]
)


async def goal_after_creating(goal_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='📅 Add monthly task', callback_data=f'create_monthly_task_{goal_id}')],
            [InlineKeyboardButton(text='🎯 Add other goal', callback_data='create_year_task')],
            [InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start')]
        ]
    )


async def monthly_task_after_creating(monthly_task_id: int, goal_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='📋 Add weekly task', callback_data=f'create_weekly_task_{monthly_task_id}')],
            [InlineKeyboardButton(text='📅 Add other monthly task', callback_data=f'create_monthly_task_{goal_id}')],
            [InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start')]
        ]
    )


async def weekly_task_after_creating(weekly_task_id: int, monthly_task_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='📋 Add daily task', callback_data=f'create_daily_task_{weekly_task_id}')],
            [InlineKeyboardButton(text='📅 Add other weekly task',
                                  callback_data=f'create_weekly_task_{monthly_task_id}')],
            [InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start')]
        ]
    )


async def goal_list(goals: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for goal in goals:
        keyboard.add(InlineKeyboardButton(text=f'🎯 {goal.title}', callback_data=f'goal_{goal.id}'))

    keyboard.add(InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start'))
    return keyboard.adjust(1).as_markup()


async def monthly_task_list(tasks: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for task in tasks:
        keyboard.add(InlineKeyboardButton(text=f'📅 {task.title}', callback_data=f'monthly_task_{task.id}'))

    keyboard.add(InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start'))
    return keyboard.adjust(1).as_markup()
