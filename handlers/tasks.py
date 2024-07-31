from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import database.requests.task as task_rq
import keyboards.tasks as task_kb

router = Router()


class CreateGoal(StatesGroup):
    name = State()


@router.message(Command("create_year_task"))
async def cmd_create_goal(message: Message, state: FSMContext):
    await message.answer("Please enter the name of your yearly goal:")
    await state.set_state(CreateGoal.name)


@router.message(CreateGoal.name)
async def process_goal_name(message: Message, state: FSMContext):
    goal_name = message.text
    user_id = message.from_user.id

    goal = await task_rq.set_year_goal(user_id, goal_name)
    await message.answer(f"Yearly goal '{goal.title}' has been created! Add your mouthly task to set your goal",
                         reply_markup=await task_kb.goal_after_creating(goal.id))
    await state.clear()


@router.callback_query(F.data == 'create_year_task')
async def callback_create_year_task(callback_query: CallbackQuery, state: FSMContext):
    # Вызов команды, которая должна выполняться при нажатии на кнопку
    await cmd_create_goal(callback_query.message, state)
    await callback_query.answer()


@router.callback_query(F.data.startswith('create_monthly_task_'))
async def notes_by_tag(callback: CallbackQuery):
    pass
