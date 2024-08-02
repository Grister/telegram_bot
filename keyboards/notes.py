from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests.note import get_tag_list, get_notes_by_tag


async def note_menu(tag_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🛠 Edit notes', callback_data=f'notes_list_{tag_id}')],
            [InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start')]
        ]
    )


async def note_context(note_id: int, tag_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✏️ Edit note', callback_data=f'edit_note_{note_id}')],
            [InlineKeyboardButton(text='🚫 Delete note', callback_data=f'del_note_{note_id}')],
            [InlineKeyboardButton(text='⬅️ Back', callback_data=f'notes_list_{tag_id}')]
        ]
    )


async def empty_note_menu(tag_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🚫 Delete tag', callback_data=f'del_tag_{tag_id}')],
            [InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start')]
        ]
    )


async def tags_list(user_id: int) -> InlineKeyboardMarkup:
    all_tags = await get_tag_list(user_id)
    keyboard = InlineKeyboardBuilder()
    for tag in all_tags:
        keyboard.add(InlineKeyboardButton(text=f'📌 {tag.name}', callback_data=f'tag_{tag.id}'))

    keyboard.add(InlineKeyboardButton(text='⬅️ Back to main', callback_data='callback_start'))
    return keyboard.adjust(2).as_markup()


async def notes_list(tag_id: int) -> InlineKeyboardMarkup:
    all_notes = await get_notes_by_tag(tag_id)
    keyboard = InlineKeyboardBuilder()
    for note in all_notes:
        keyboard.add(InlineKeyboardButton(
            text=f"🖋 {note.content[:20]}",
            callback_data=f'note_{note.id}'))

    keyboard.add(InlineKeyboardButton(text='⬅️ Back', callback_data=f'tag_{tag_id}'))
    return keyboard.adjust(1).as_markup()
