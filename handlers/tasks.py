from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import database.requests.task as task_rq
import keyboards.tasks as task_kb
from database.models import StatusEnum

router = Router()


class CreateTask(StatesGroup):
    title = State()


@router.message(Command("tasks"))
async def cmd_get_tasks(message: Message, user_id: int = None):
    user_id = user_id if user_id else message.from_user.id
    tasks = await task_rq.get_task_list(user_id)

    if tasks:
        await message.answer(
            text="Here is your tasks. Click on task to edit the task",
            reply_markup=await task_kb.task_list(user_id)
        )
    else:
        await message.answer(
            text="You don't have any tasks. To create a task you can use command '/create_task' "
                 "or click on button below",
            reply_markup=task_kb.empty_tasks_menu
        )


@router.message(Command('task_archive'))
async def cmd_task_archive(message: Message):
    tasks = await task_rq.get_task_list(message.from_user.id)

    msg = "Archive tasks:\n\n"
    for task in tasks:
        if task.status == StatusEnum.COMPLETED:
            msg += f"✅ {task.title}\n"
        elif task.status == StatusEnum.CANCELED:
            msg += f"❌ {task.title}\n"

    await message.answer(msg)


# Make new note
@router.message(F.text.startswith('!'))
async def create_task(message: Message):
    user_id = message.from_user.id
    task_title = message.text[1:]

    await task_rq.set_daily_task(user_id, task_title)
    await message.reply("Note was saved successfully ✅")


@router.message(Command("create_task"))
async def cmd_create_task(message: Message, state: FSMContext):
    await message.answer("Please enter the name of your task:")
    await state.set_state(CreateTask.title)


@router.message(CreateTask.title)
async def process_goal_name(message: Message, state: FSMContext):
    task_title = message.text
    user_id = message.from_user.id
    task = await task_rq.set_daily_task(user_id, task_title)

    await message.answer(
        text=f"Task '{task.title}' has been created!",
        reply_markup=task_kb.task_after_creating_menu
    )
    await state.clear()


@router.callback_query(F.data == 'create_task')
async def callback_create_task(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_create_task(callback.message, state)


# Get specific task
@router.callback_query(F.data.startswith('task_'))
async def note_context(callback: CallbackQuery):
    task = await task_rq.get_task_instance(int(callback.data.split('_')[1]))

    await callback.answer()
    await callback.message.edit_text(
        text=f'✔️ {task.title}',
        reply_markup=await task_kb.task_context(task.id)
    )


# Complete specific task
@router.callback_query(F.data.startswith('complete_task_'))
async def task_complete(callback: CallbackQuery):
    task_id = int(callback.data.split('_')[2])
    await task_rq.set_task_status(task_id, StatusEnum.COMPLETED)
    await callback.answer("Note was completed")
    await cmd_get_tasks(callback.message, callback.from_user.id)


# Cancel specific task
@router.callback_query(F.data.startswith('cancel_task_'))
async def task_cancel(callback: CallbackQuery):
    task_id = int(callback.data.split('_')[2])
    await task_rq.set_task_status(task_id, StatusEnum.CANCELED)
    await callback.answer("Note was canceled")
    await cmd_get_tasks(callback.message, callback.from_user.id)
