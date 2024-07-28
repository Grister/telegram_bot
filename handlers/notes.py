from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import keyboards.notes as notes_kb
import database.requests as rq

router = Router()


@router.message(F.text.startswith('#'))
async def add_note(message: Message):
    user_id = message.from_user.id
    parts = message.text[1:].split(maxsplit=1)

    if len(parts) < 2:
        await message.reply("Failed to recognize the note. Please use the format: #tag note.")
        return

    tag, content = parts
    await rq.note.set_note(user_id, tag, content)
    await message.answer("Note was saved successfully")


@router.message(Command('tags'))
async def cmd_get_tags(message: Message):
    await message.answer(
        text="Here is yours tags. Pick the tag to see notes by tag. "
             "You can create new note using the format: #tag note.",
        reply_markup=await notes_kb.tags_kb(message.from_user.id)
    )


@router.callback_query(F.data.startswith('tag_'))
async def notes_by_tag(callback: CallbackQuery):
    tag = await rq.note.get_tag(int(callback.data.split('_')[1]))
    notes = await rq.note.get_notes_by_tag(tag.id)

    notes_message = f"Notes with tag #{tag.name}:\n\n"
    for note in notes:
        notes_message += f"Date: {note.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        notes_message += f"- {note.content}\n\n"

    await callback.answer(f"You chose tag '{tag.name}'")
    await callback.message.answer(notes_message, reply_markup=await notes_kb.get_note_menu(tag.id))


@router.callback_query(F.data.startswith('note_editor_'))
async def notes_list(callback: CallbackQuery):
    tag_id = int(callback.data.split('_')[2])
    await callback.answer("")
    await callback.message.answer(text="Pick the note", reply_markup=await notes_kb.notes_list(tag_id))


@router.callback_query(F.data.startswith('note_'))
async def note_editor(callback: CallbackQuery):
    note = await rq.note.get_note(int(callback.data.split('_')[1]))
    await callback.answer('')
