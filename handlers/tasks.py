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


class CreateTask(StatesGroup):
    parent_id: int
    name = State()


class MonthlyTask(CreateTask):
    pass


class WeeklyTask(CreateTask):
    pass


@router.message(Command("tasks"))
async def cmd_get_tasks(message: Message, user_id: int = None):
    goals = await task_rq.get_goal_list(user_id if user_id else message.from_user.id)
    if goals:
        await message.answer(f"Here is your year goals. Click on goal to see tasks by this goal",
                             reply_markup=await task_kb.goal_list(goals))
    else:
        await message.answer("You don't have any goals. To create a goal you can use command '/create_year_task' "
                             "or click on button below",
                             reply_markup=task_kb.empty_goals_menu)


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
async def callback_create_year_task(callback: CallbackQuery, state: FSMContext):
    await cmd_create_goal(callback.message, state)
    await callback.answer()


@router.callback_query(F.data.startswith('create_monthly_task_'))
async def create_monthly_task(callback: CallbackQuery, state: FSMContext):
    goal_id = int(callback.data.split('_')[3])

    await state.set_state(MonthlyTask.name)
    await state.update_data(parent_id=goal_id)
    await callback.message.answer("Please enter the title of your monthly task:")


@router.message(MonthlyTask.name)
async def process_monthly_task_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    data = await state.get_data()
    task = await task_rq.set_monthly_task(goal_id=data['parent_id'], task_name=data['name'])

    await message.answer(
        text=f"Monthly task '{task.title}' has been created! Add your weekly task to set your goal",
        reply_markup=await task_kb.monthly_task_after_creating(task.id, data['parent_id'])
    )
    await state.clear()


@router.callback_query(F.data.startswith('create_weekly_task_'))
async def create_weekly_task(callback: CallbackQuery, state: FSMContext):
    monthly_task_id = int(callback.data.split('_')[3])

    await state.set_state(WeeklyTask.name)
    await state.update_data(parent_id=monthly_task_id)
    await callback.message.answer("Please enter the title of your weekly task:")


@router.message(WeeklyTask.name)
async def process_weekly_task_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    data = await state.get_data()
    task = await task_rq.set_weekly_task(monthly_task_id=data['parent_id'], task_name=data['name'])

    await message.answer(
        text=f"Weekly task '{task.title}' has been created! Add your daily task to start your way nahui",
        reply_markup=await task_kb.weekly_task_after_creating(task.id, data['parent_id'])
    )
    await state.clear()


@router.callback_query(F.data.startswith('goal_'))
async def monthly_tasks(callback: CallbackQuery):
    goal_id = int(callback.data.split('_')[1])
    goal = await task_rq.get_goal_instance(goal_id)
    tasks = await task_rq.get_monthly_task_list(goal_id)

    await callback.answer()
    await callback.message.answer(
        text=f'Here is your monthly tasks from {goal.title}',
        reply_markup=await task_kb.monthly_task_list(tasks)
    )
