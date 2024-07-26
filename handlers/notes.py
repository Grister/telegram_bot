from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import keyboards.notes as kb
from database.requests import user, note

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    await user.set_user(user_id, username)
    await message.answer(f'Hello, {message.from_user.first_name}! '
                         f'How can I help you?',
                         reply_markup=kb.main)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Helper doc')


@router.message(F.text.startswith('#'))
async def add_note(message: Message):
    user_id = message.from_user.id
    parts = message.text[1:].split(maxsplit=1)

    if len(parts) < 2:
        await message.reply("Failed to recognize the note. Please use the format: #tag note.")
        return

    tag, content = parts
    await note.set_note(user_id, tag, content)
    await message.answer("Note was saved successfully")


@router.message(Command('tags'))
async def cmd_get_tags(message: Message):
    tags_list = await note.get_tags(message.from_user.id)
    for tag in tags_list:
        print(tag.name)

    await message.answer(
        text=f'{tags_list.all()}'
    )
