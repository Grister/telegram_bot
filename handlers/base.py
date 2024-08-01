import random

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.formatting import Code
from aiogram.enums import ParseMode

import keyboards.main as kb
import database.requests.user as user_rq
from utils.password_generate import generate_password

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

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
        '/currency - Get currency rates ',
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
