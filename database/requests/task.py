from typing import Optional, List
from sqlalchemy import select, delete, update, text

from database.db import async_session
from database.models import DailyTask, StatusEnum
import utils.db_utils as db_tools


async def set_daily_task(user_id: int, task_name: str) -> Optional[DailyTask]:
    async with async_session() as session:
        user = await db_tools.get_user_by_id(session, user_id)
        return await db_tools.create_instance(session, DailyTask, user_id=user.id, title=task_name)


async def get_task_list(user_id: int) -> List[DailyTask]:
    async with async_session() as session:
        user = await db_tools.get_user_by_id(session, user_id)
        ordering = text("created_at DESC")
        return await db_tools.get_list(session, DailyTask, order_by=ordering, user_id=user.id)


async def get_task_instance(task_id: int) -> Optional[DailyTask]:
    async with async_session() as session:
        return await db_tools.get_instance(session, DailyTask, id=task_id)


async def set_task_status(task_id: int, status: StatusEnum) -> None:
    async with async_session() as session:
        await session.execute(
            update(DailyTask)
            .where(DailyTask.id == task_id)
            .values(status=status)
            .returning(DailyTask)
        )
        await session.commit()
