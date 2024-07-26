from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import keyboards.notes as kb
from database.requests import user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    id = message.from_user.id
    username = message.from_user.username

    await user.set_user(id, username)
    await message.answer(f'Hello! {message.from_user.first_name}',
                         reply_markup=kb.main)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Helper doc')


@router.message(F.text == 'how are you?')
async def cmd_how_are_you(message: Message):
    await message.answer("I'm fine")


@router.message(F.photo)
async def cmd_get_photo(message: Message):
    await message.answer(f'ID photo = {message.photo[-1].file_id}')


@router.message(Command('get_photo'))
async def send_photo(message: Message):
    await message.answer_photo(
        photo='AgACAgIAAxkBAAMVZp_Roo-jxhbimhMiYw-Gnd2Ypb0AAn7cMRvutvhIaGBrVsTH9X0BAAMCAAN5AAM1BA',
        caption='It\'s a photo'
    )


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('answer', show_alert=True)
    await callback.message.edit_text('Hello, chepuha!', reply_markup=await kb.inline_cars())
