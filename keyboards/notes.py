from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database.requests.note import get_tags, get_notes_by_tag

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Check scu', callback_data='catalog')],
    [InlineKeyboardButton(text='Your notes', callback_data='basket'),
     InlineKeyboardButton(text='Contacts', callback_data='contacts')]
])


async def note_menu(tag_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Edit notes', callback_data=f'note_editor_{tag_id}')],
            [InlineKeyboardButton(text='Back to main', callback_data='to_main')]
        ]
    )


async def tags_kb(user_id: int) -> InlineKeyboardMarkup:
    all_tags = await get_tags(user_id)
    keyboard = InlineKeyboardBuilder()
    for tag in all_tags:
        keyboard.add(InlineKeyboardButton(text=tag.name, callback_data=f'tag_{tag.id}'))

    keyboard.add(InlineKeyboardButton(text='To main', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def notes_list(tag_id: int) -> InlineKeyboardMarkup:
    all_notes = await get_notes_by_tag(tag_id)
    keyboard = InlineKeyboardBuilder()
    for note in all_notes:
        keyboard.add(InlineKeyboardButton(
            text=f"Date: {note.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                 f"- {note.content}",
            callback_data=f'note_{note.id}'))

    keyboard.add(InlineKeyboardButton(text='Back', callback_data=f'tag_{tag_id}'))
    return keyboard.adjust(1).as_markup()
