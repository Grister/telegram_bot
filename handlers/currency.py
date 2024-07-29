from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from services.currency_service import collect_rates
from utils.text_formaters import format_currency_data

router = Router()


# Make new note
@router.message(Command('currency'))
async def cmd_get_rates(message: Message):
    formatted_data = format_currency_data(await collect_rates())
    await message.answer(formatted_data, parse_mode=ParseMode.HTML)
