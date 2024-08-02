from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Code
from aiogram.enums import ParseMode

import keyboards.main as kb
import database.requests.user as user_rq

from handlers.currency import cmd_get_rates
from handlers.notes import cmd_get_tags

from utils.password_generate import generate_password

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, user_id: int = None, username: str = None):
    user_id = user_id if user_id else message.from_user.id
    username = username if username else message.from_user.username

    await user_rq.set_user(user_id, username)
    await message.answer(f'Hello, {message.from_user.first_name}! '
                         f'How can I help you?',
                         reply_markup=kb.main)


@router.message(Command('help'))
async def cmd_help(message: Message):
    text = [
        'Command list: ',
        '/start - Начать диалог',
        '/password - Generate new password. You can add argument `length` after command.'
        'Example: /password 16',
        '/currency - Get currency rates',
        '/tags - Get notes by tags',
    ]
    await message.answer('\n'.join(text))


@router.message(Command('password'))
async def cmd_password(message: Message):
    length = 8
    try:
        arg = message.text.split()[1]
        if arg.isdigit():
            length = int(arg)
    except Exception as e:
        pass

    password = generate_password(length)

    await message.answer(
        text=f'Here is your {length}-character password. Click on text to copy it:\n'
             f'{Code(password).as_markdown()}',
        parse_mode=ParseMode.MARKDOWN
    )


@router.callback_query(F.data == 'callback_currency')
async def callback_currency(callback: CallbackQuery):
    await cmd_get_rates(callback.message)


@router.callback_query(F.data == 'callback_password')
async def callback_password(callback: CallbackQuery):
    await cmd_password(callback.message)


@router.callback_query(F.data == 'callback_start')
async def callback_start(callback: CallbackQuery):
    await cmd_start(
        callback.message,
        user_id=callback.from_user.id,
        username=callback.from_user.username
    )


@router.callback_query(F.data == 'callback_tags')
async def callback_tags(callback: CallbackQuery):
    await cmd_get_tags(callback.message, user_id=callback.from_user.id)
