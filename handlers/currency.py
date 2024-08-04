from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from services.currency_service import collect_rates
from utils.text_formaters import format_currency_data

router = Router()


@router.message(Command('currency'))
async def cmd_get_rates(message: Message):
    await message.answer("Wait a second...⏳")
    formatted_data = format_currency_data(await collect_rates())
    await message.answer(formatted_data, parse_mode=ParseMode.HTML)
