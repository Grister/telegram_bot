from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import StatusEnum
from database.requests.task import get_task_list

empty_tasks_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='☑️ Add new task', callback_data='create_task')],
        [InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start')]
    ]
)

task_after_creating_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='☑️ Add new task', callback_data='create_task')],
        [InlineKeyboardButton(text='✔️ Check your tasks', callback_data='callback_tasks')],
        [InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start')]
    ]
)


async def task_context(task_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✅ Complete task', callback_data=f'complete_task_{task_id}')],
            [InlineKeyboardButton(text='🚫 Cancel task', callback_data=f'cancel_task_{task_id}')],
            [InlineKeyboardButton(text='⬅️ Back', callback_data='callback_tasks')]
        ]
    )


async def task_list(user_id: int) -> InlineKeyboardMarkup:
    all_tasks = await get_task_list(user_id)
    keyboard = InlineKeyboardBuilder()
    for task in all_tasks:
        if task.status == StatusEnum.IN_PROGRESS:
            keyboard.add(InlineKeyboardButton(text=f'✔️ {task.title}', callback_data=f'task_{task.id}'))
    keyboard.add(InlineKeyboardButton(text='☑️ Create new task', callback_data='create_task'))
    keyboard.add(InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start'))
    return keyboard.adjust(1).as_markup()
