from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Italic
from aiogram.enums import ParseMode

import keyboards.notes as notes_kb
import database.requests as rq

router = Router()


class EditNote(StatesGroup):
    note_id = int
    content = State()


# Make new note
@router.message(F.text.startswith('#'))
async def add_note(message: Message):
    user_id = message.from_user.id
    parts = message.text[1:].split(maxsplit=1)

    if len(parts) < 2:
        await message.reply("❗️Failed to recognize the note. Please use the format: #tag note.")
        return

    tag, content = parts
    await rq.note.set_note(user_id, tag, content)
    await message.reply("Note was saved successfully ✅")


# Get list of your tags
@router.message(Command('tags'))
async def cmd_get_tags(message: Message):
    await message.answer(
        text="Here are your tags. Select a tag to view the notes associated with it. "
             "To create a new note, use the format: #tag note.",
        reply_markup=await notes_kb.tags_list(message.from_user.id)
    )


# List of notes by tag in one message
@router.callback_query(F.data.startswith('tag_'))
async def notes_by_tag(callback: CallbackQuery):
    tag = await rq.note.get_tag(int(callback.data.split('_')[1]))
    notes = await rq.note.get_notes_by_tag(tag.id)

    notes_message = f"Notes with tag #{tag.name}:\n\n"
    for note in notes:
        notes_message += f"🕝 {Italic(note.created_at.strftime('%d/%m/%Y %H:%M')).as_markdown()}\n"
        notes_message += f"\t - {note.content}\n\n"
    await callback.answer(f"You selected the tag '{tag.name}'")
    await callback.message.answer(
        notes_message,
        reply_markup=await notes_kb.note_menu(tag.id),
        parse_mode=ParseMode.MARKDOWN
    )


# List of notes as keyboard
@router.callback_query(F.data.startswith('notes_list_'))
async def notes_list(callback: CallbackQuery):
    tag_id = int(callback.data.split('_')[2])
    await callback.answer("")
    await callback.message.edit_text(
        text="Select a note to view or edit it:",
        reply_markup=await notes_kb.notes_list(tag_id)
    )


# Get specific note
@router.callback_query(F.data.startswith('note_'))
async def note_context(callback: CallbackQuery):
    note = await rq.note.get_note(int(callback.data.split('_')[1]))

    await callback.answer("")
    await callback.message.answer(
        text=f'🕝 {note.created_at.strftime("%Y-%m-%d %H:%M")} \n 🔸 {note.content}',
        reply_markup=await notes_kb.note_context(note.id)
    )


# Delete specific note
@router.callback_query(F.data.startswith('del_note_'))
async def note_delete(callback: CallbackQuery):
    await rq.note.delete_note(int(callback.data.split('_')[2]))
    await callback.answer("Note was deleted", show_alert=True)


# Update specific note
@router.callback_query(F.data.startswith('edit_note_'))
async def note_edit(callback: CallbackQuery, state: FSMContext):
    note = await rq.note.get_note(int(callback.data.split('_')[2]))

    await state.set_state(EditNote.content)
    await state.update_data(note_id=note.id)
    await callback.message.answer('Please enter the new text for the note below:')


@router.message(EditNote.content)
async def save(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    data = await state.get_data()
    await rq.note.update_note(note_id=data['note_id'], new_content=data['content'])

    await state.clear()
    await message.answer("Update was saved ✅")
