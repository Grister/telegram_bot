from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import Code

import database.requests.user as user_rq
import keyboards.main as kb
from handlers.currency import cmd_get_rates
from handlers.notes import cmd_get_tags
from handlers.tasks import cmd_get_tasks
from utils.password_generate import generate_password

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, user_id: int = None, username: str = None, from_callback: bool = False):
    user_id = user_id if user_id else message.from_user.id
    username = username if username else message.from_user.username

    if from_callback:
        await message.edit_text(
            text='How can I help you next?',
            reply_markup=kb.main
        )
    else:
        await user_rq.set_user(user_id, username)
        await message.answer(
            text=f'Hello, {message.from_user.first_name}! '
                 f'How can I help you?',
            reply_markup=kb.main
        )


@router.message(Command('help'))
async def cmd_help(message: Message):
    text = [
        'Command list: ',
        '/start - Начать диалог',
        '/password - Generate new password. You can add argument `length` after command. '
        'Example: `/password 16`',
        '/currency - Get currency rates',
        '/tags - Get notes by tags',
        '/tasks - Check your daily tasks',
        '/create_task - Create new daily task',
        '/task_archive - Get task archive',
    ]
    await message.answer('\n'.join(text))


@router.message(Command('password'))
async def cmd_password(message: Message):
    length = 8
    try:
        arg = message.text.split()[1]
        if arg.isdigit():
            length = int(arg)
    except Exception:
        pass

    password = generate_password(length)

    await message.answer(
        text=f'Here is your {length}-character password. Click on text to copy it:\n'
             f'{Code(password).as_markdown()}',
        parse_mode=ParseMode.MARKDOWN
    )


@router.callback_query(F.data == 'callback_currency')
async def callback_currency(callback: CallbackQuery):
    await callback.answer()
    await cmd_get_rates(callback.message)


@router.callback_query(F.data == 'callback_password')
async def callback_password(callback: CallbackQuery):
    await callback.answer()
    await cmd_password(callback.message)


@router.callback_query(F.data == 'callback_start')
async def callback_start(callback: CallbackQuery):
    await callback.answer()
    await cmd_start(
        callback.message,
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        from_callback=True
    )


@router.callback_query(F.data == 'callback_tags')
async def callback_tags(callback: CallbackQuery):
    await callback.answer()
    await cmd_get_tags(callback.message, user_id=callback.from_user.id)


@router.callback_query(F.data == 'callback_tasks')
async def callback_tasks(callback: CallbackQuery):
    await callback.answer()
    await cmd_get_tasks(callback.message, user_id=callback.from_user.id)
