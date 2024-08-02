from typing import Optional, List

from database.db import async_session
from database.models import Goal, MonthlyTask, WeeklyTask, DailyTask
import utils.db_utils as db_tools
from sqlalchemy import select, delete, update


async def set_year_goal(user_id: int, goal_name: str) -> Optional[Goal]:
    async with async_session() as session:
        user = await db_tools.get_user_by_id(session, user_id)
        return await db_tools.create_instance(session, Goal, user_id=user.id, title=goal_name)


async def set_monthly_task(goal_id: int, task_name: str) -> Optional[MonthlyTask]:
    async with async_session() as session:
        return await db_tools.create_instance(session, MonthlyTask, goal_id=goal_id, title=task_name)


async def set_weekly_task(monthly_task_id: int, task_name: str) -> Optional[WeeklyTask]:
    async with async_session() as session:
        return await db_tools.create_instance(session, WeeklyTask, monthly_task_id=monthly_task_id, title=task_name)


async def get_goal_list(user_id: int) -> List[Goal]:
    async with async_session() as session:
        user = await db_tools.get_user_by_id(session, user_id)
        return await db_tools.get_list(session, Goal, user_id=user.id)


async def get_goal_instance(goal_id: int) -> Optional[Goal]:
    async with async_session() as session:
        return await db_tools.get_instance(session, Goal, id=goal_id)


async def get_monthly_task_list(goal_id: int) -> List[MonthlyTask]:
    async with async_session() as session:
        return await db_tools.get_list(session, MonthlyTask, goal_id=goal_id)


async def get_monthly_task_instance(task_id: int) -> Optional[MonthlyTask]:
    async with async_session() as session:
        return await db_tools.get_instance(session, MonthlyTask, id=task_id)
