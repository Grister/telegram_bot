import random

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode

import keyboards.main as kb
import database.requests.user as user_rq

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
    chars = '+-/!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = 8
    password = ''
    try:
        arg = message.text.split()[1]
        if arg.isdigit():
            length = int(arg)
    except Exception as e:
        pass

    for i in range(length):
        password += random.choice(chars)

    await message.answer(
        text=f'Here is your {length}-character password. Click on text to copy it:\n'
             f'`{password}`',
        parse_mode=ParseMode.MARKDOWN_V2
    )
