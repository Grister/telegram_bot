from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from database.requests.note import get_tags, get_notes_by_tag

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Some catalog', callback_data='catalog')],
    [InlineKeyboardButton(text='Basket', callback_data='basket'),
     InlineKeyboardButton(text='Contacts', callback_data='contacts')]
])

note_menu = InlineKeyboardMarkup(  # TODO
    inline_keyboard=[
        [InlineKeyboardButton(text='Edit notes', callback_data='note_editor')],
        [InlineKeyboardButton(text='Back to main', callback_data='to_main')]
    ]
)


async def tags_kb(user_id: int):
    all_tags = await get_tags(user_id)
    keyboard = InlineKeyboardBuilder()
    for tag in all_tags:
        keyboard.add(InlineKeyboardButton(text=tag.name, callback_data=f'tag_{tag.id}'))

    keyboard.add(InlineKeyboardButton(text='To main', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def notes_editor(tag_id: int):
    all_notes = await get_notes_by_tag(tag_id)
    keyboard = InlineKeyboardBuilder()
    for note in all_notes:
        keyboard.add(InlineKeyboardButton(
            text=f"Date: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                 f"- {note.content}",
            callback_data=f'note_{note.id}'))

    keyboard.add(InlineKeyboardButton(text='To main', callback_data='to_main'))
    return keyboard.adjust(1).as_markup()
